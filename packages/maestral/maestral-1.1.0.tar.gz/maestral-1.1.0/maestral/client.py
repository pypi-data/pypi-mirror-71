# -*- coding: utf-8 -*-
"""
@author: Sam Schott  (ss2151@cam.ac.uk)

(c) Sam Schott; This work is licensed under the MIT licence.

This modules contains the Dropbox API client. It wraps calls to the Dropbox Python SDK
and handles exceptions, chunked uploads or downloads, etc.

"""

# system imports
import os
import os.path as osp
import time
import logging
import functools
import contextlib
from datetime import datetime, timezone

# external imports
import requests
from dropbox import Dropbox, dropbox, files, users, exceptions

# local imports
from maestral import __version__
from maestral.config import MaestralState
from maestral.errors import SyncError, dropbox_to_maestral_error, os_to_maestral_error


logger = logging.getLogger(__name__)

# create single requests session for all clients
SESSION = dropbox.create_session()
_major_minor_version = '.'.join(__version__.split('.')[:2])
USER_AGENT = f'Maestral/v{_major_minor_version}'


CONNECTION_ERRORS = (
    requests.exceptions.Timeout,
    requests.exceptions.RetryError,
    requests.exceptions.ChunkedEncodingError,
    requests.exceptions.ConnectionError,
    ConnectionError,
)


def natural_size(num, unit='B', sep=True):
    """
    Convert number to a human readable string with decimal prefix.

    :param float num: Value in given unit.
    :param str unit: Unit suffix.
    :param bool sep: Whether to separate unit and value with a space.
    :returns: Human readable string with decimal prefixes.
    :rtype: str
    """
    sep = ' ' if sep else ''

    for prefix in ('', 'K', 'M', 'G'):
        if abs(num) < 1000.0:
            return f'{num:3.1f}{sep}{prefix}{unit}'
        num /= 1000.0

    prefix = 'T'
    return f'{num:.1f}{sep}{prefix}{unit}'


class SpaceUsage(users.SpaceUsage):

    def allocation_type(self):
        if self.allocation.is_team():
            return 'team'
        elif self.allocation.is_individual():
            return 'individual'
        else:
            return ''

    def __str__(self):

        if self.allocation.is_individual():
            used = self.used
            allocated = self.allocation.get_individual().allocated
        elif self.allocation.is_team():
            used = self.allocation.get_team().used
            allocated = self.allocation.get_team().allocated
        else:
            return natural_size(self.used)

        percent = used / allocated
        return f'{percent:.1%} of {natural_size(allocated)} used'


def to_maestral_error(dbx_path_arg=None, local_path_arg=None):
    """
    Returns a decorator that converts instances of :class:`OSError` and
    :class:`exceptions.DropboxException` to :class:`errors.MaestralApiError`.

    :param int dbx_path_arg: Argument number to take as dbx_path for exception.
    :param int local_path_arg: Argument number to take as local_path_arg for exception.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            dbx_path = args[dbx_path_arg] if dbx_path_arg else None
            local_path = args[local_path_arg] if local_path_arg else None

            try:
                return func(*args, **kwargs)
            except exceptions.DropboxException as exc:
                raise dropbox_to_maestral_error(exc, dbx_path, local_path)
            # catch connection errors first, they may inherit from OSError
            except CONNECTION_ERRORS:
                raise ConnectionError('Cannot connect to Dropbox')
            except OSError as exc:
                raise os_to_maestral_error(exc, dbx_path, local_path)

        return wrapper

    return decorator


class DropboxClient:
    """Client for the Dropbox SDK.

    This client defines basic methods to wrap Dropbox Python SDK calls, such as creating,
    moving, modifying and deleting files and folders on Dropbox and downloading files from
    Dropbox.

    All Dropbox SDK exceptions and :class:`OSError` instances if related to accessing or
    saving local files will be caught and reraised as a :class:`errors.MaestralApiError`.
    Connection errors from requests will be caught and reraised as
    :class:`ConnectionError`.

    :param str config_name: Name of config file and state file to use.
    :param str access_token: Dropbox access token for user.
    :param int timeout: Timeout for individual requests. Defaults to 100 sec if not given.
    """

    SDK_VERSION = '2.0'

    def __init__(self, config_name, access_token, timeout=100):

        self.config_name = config_name

        self._state = MaestralState(config_name)
        self._backoff_until = 0

        # initialize API client
        self.dbx = Dropbox(
            access_token,
            session=SESSION,
            user_agent=USER_AGENT,
            timeout=timeout
        )

    def set_access_token(self, token):
        self.dbx._oauth2_access_token = token

    @to_maestral_error()
    def get_account_info(self, dbid=None):
        """
        Gets current account information.

        :param str dbid: Dropbox ID of account. If not given, will get the info of the
            currently linked account.
        :returns: Account info.
        :rtype: :class:`users.FullAccount`
        """
        if dbid:
            res = self.dbx.users_get_account(dbid)
        else:
            res = self.dbx.users_get_current_account()

        if not dbid:
            # save our own account info to config
            if res.account_type.is_basic():
                account_type = 'basic'
            elif res.account_type.is_business():
                account_type = 'business'
            elif res.account_type.is_pro():
                account_type = 'pro'
            else:
                account_type = ''

            self._state.set('account', 'email', res.email)
            self._state.set('account', 'display_name', res.name.display_name)
            self._state.set('account', 'abbreviated_name', res.name.abbreviated_name)
            self._state.set('account', 'type', account_type)

        return res

    @to_maestral_error()
    def get_space_usage(self):
        """
        Gets current account space usage.

        :returns: :class:`SpaceUsage` instance.
        :rtype: :class:`SpaceUsage`
        """
        res = self.dbx.users_get_space_usage()

        # convert from users.SpaceUsage to SpaceUsage
        res.__class__ = SpaceUsage

        # save results to config
        self._state.set('account', 'usage', str(res))
        self._state.set('account', 'usage_type', res.allocation_type())

        return res

    @to_maestral_error()
    def unlink(self):
        """
        Unlinks the Dropbox account.
        """
        self.dbx.auth_token_revoke()  # should only raise auth errors

    @to_maestral_error(dbx_path_arg=1)
    def get_metadata(self, dbx_path, **kwargs):
        """
        Gets metadata for an item on Dropbox or returns ``False`` if no metadata is
        available. Keyword arguments are passed on to Dropbox SDK files_get_metadata call.

        :param str dbx_path: Path of folder on Dropbox.
        :param kwargs: Keyword arguments for Dropbox SDK files_download_to_file.
        :returns: Metadata of item at the given path or ``None``.
        :rtype: :class:`files.Metadata`
        """

        try:
            return self.dbx.files_get_metadata(dbx_path, **kwargs)
        except exceptions.ApiError:
            # DropboxAPI error is only raised when the item does not exist on Dropbox
            # this is handled on a DEBUG level since we use call `get_metadata` to check
            # if a file exists
            pass

    @to_maestral_error(dbx_path_arg=1)
    def list_revisions(self, dbx_path, mode='path', limit=10):
        """
        Lists all file revisions for the given file.

        :param str dbx_path: Path to file on Dropbox.
        :param str mode: Must be 'path' or 'id'. If 'id', specify the Dropbox file ID
            instead of the file path to get revisions across move and rename events.
        :param int limit: Maximum number of revisions to list. Defaults to 10.
        :returns: File revision history.
        :rtype: :class:`files.ListRevisionsResult`
        """

        mode = files.ListRevisionsMode(mode)
        return self.dbx.files_list_revisions(dbx_path, mode=mode, limit=limit)

    @to_maestral_error(dbx_path_arg=1)
    def restore(self, dbx_path, rev):
        """
        Restore an old revision of a file.

        :param str dbx_path: The path to save the restored file.
        :param str rev: The revision to restore. Old revisions can be listed with
            :meth:`list_revisions`.
        :returns: Metadata of restored file.
        :rtype: :class:`files.FileMetadata`
        """

        return self.dbx.files_restore(dbx_path, rev)

    @to_maestral_error(dbx_path_arg=1)
    def download(self, dbx_path, local_path, **kwargs):
        """
        Downloads file from Dropbox to our local folder.

        :param str dbx_path: Path to file on Dropbox or rev number.
        :param str local_path: Path to local download destination.
        :param kwargs: Keyword arguments for Dropbox SDK files_download_to_file.
        :returns: Metadata of downloaded item.
        :rtype: :class:`files.FileMetadata`
        """
        # create local directory if not present
        dst_path_directory = osp.dirname(local_path)
        try:
            os.makedirs(dst_path_directory)
        except FileExistsError:
            pass

        md, http_resp = self.dbx.files_download(dbx_path, **kwargs)

        chunksize = 2 ** 16
        size_str = natural_size(md.size)

        downloaded = 0

        with open(local_path, 'wb') as f:
            with contextlib.closing(http_resp):
                for c in http_resp.iter_content(chunksize):
                    if md.size > 5 * 10 ** 6:  # 5 MB
                        logger.info(f'Downloading {natural_size(downloaded)}/{size_str}...')
                    f.write(c)
                    downloaded += chunksize

        # dropbox SDK provides naive datetime in UTC
        client_mod_timestamp = md.client_modified.replace(tzinfo=timezone.utc).timestamp()
        server_mod_timestamp = md.server_modified.replace(tzinfo=timezone.utc).timestamp()

        # enforce client_modified < server_modified
        timestamp = min(client_mod_timestamp, server_mod_timestamp, time.time())
        # set mtime of downloaded file
        os.utime(local_path, (time.time(), timestamp))

        return md

    @to_maestral_error(local_path_arg=1, dbx_path_arg=2)
    def upload(self, local_path, dbx_path, chunk_size_mb=5, **kwargs):
        """
        Uploads local file to Dropbox.

        :param str local_path: Path of local file to upload.
        :param str dbx_path: Path to save file on Dropbox.
        :param kwargs: Keyword arguments for Dropbox SDK files_upload.
        :param int chunk_size_mb: Maximum size for individual uploads in MB. If larger
            than 150 MB, it will be set to 150 MB.
        :returns: Metadata of uploaded file.
        :rtype: :class:`files.FileMetadata`
        """

        chunk_size_mb = clamp(chunk_size_mb, 0.1, 150)
        chunk_size = chunk_size_mb * 10**6  # convert to bytes

        size = osp.getsize(local_path)
        size_str = natural_size(size)

        # dropbox SDK takes naive datetime in UTC
        mtime = osp.getmtime(local_path)
        mtime_dt = datetime.utcfromtimestamp(mtime)

        if size <= chunk_size:
            with open(local_path, 'rb') as f:
                md = self.dbx.files_upload(
                    f.read(), dbx_path, client_modified=mtime_dt, **kwargs
                )
            return md
        else:
            # Note: We currently do not support resuming interrupted uploads. Dropbox
            # keeps upload sessions open for 48h so this could be done in the future.
            with open(local_path, 'rb') as f:
                session_start = self.dbx.files_upload_session_start(f.read(chunk_size))
                cursor = files.UploadSessionCursor(
                    session_id=session_start.session_id,
                    offset=f.tell()
                )
                commit = files.CommitInfo(
                    path=dbx_path, client_modified=mtime_dt, **kwargs
                )

                while True:
                    try:
                        if size - f.tell() <= chunk_size:
                            md = self.dbx.files_upload_session_finish(
                                f.read(chunk_size),
                                cursor,
                                commit
                            )

                            return md

                        else:
                            self.dbx.files_upload_session_append_v2(
                                f.read(chunk_size),
                                cursor
                            )
                            cursor.offset = f.tell()
                        logger.info(f'Uploading {natural_size(f.tell())}/{size_str}...')
                    except exceptions.DropboxException as exc:
                        error = exc.error
                        if (isinstance(error, files.UploadSessionFinishError)
                                and error.is_lookup_failed()):
                            session_lookup_error = error.get_lookup_failed()
                        elif isinstance(error, files.UploadSessionLookupError):
                            session_lookup_error = error
                        else:
                            raise exc

                        if session_lookup_error.is_incorrect_offset():
                            o = session_lookup_error.get_incorrect_offset().correct_offset
                            # reset position in file
                            f.seek(o)
                            cursor.offset = f.tell()
                        else:
                            raise exc

    @to_maestral_error(dbx_path_arg=1)
    def remove(self, dbx_path, **kwargs):
        """
        Removes a file / folder from Dropbox.

        :param str dbx_path: Path to file on Dropbox.
        :param kwargs: Keyword arguments for Dropbox SDK files_delete_v2.
        :returns: Metadata of deleted item.
        :rtype: :class:`files.Metadata`
        """
        # try to remove file (response will be metadata, probably)
        res = self.dbx.files_delete_v2(dbx_path, **kwargs)
        md = res.metadata

        return md

    @to_maestral_error()
    def remove_batch(self, entries, batch_size=900):
        """
        Delete multiple items on Dropbox in a batch job.

        :param list[tuple[str, str]] entries: List of Dropbox paths and "rev"s to delete.
            If a "rev" is not None, the file will only be deleted if it matches the rev on
            Dropbox. This is not supported when deleting a folder.
        :param int batch_size: Number of items to delete in each batch. Dropbox allows
            batches of up to 1,000 items. Larger values will be capped automatically.
        :returns: List of Metadata for deleted items or :class:`errors.SyncError` for
            failures. Results will be in the same order as the original input.
        :rtype: list
        """

        batch_size = clamp(batch_size, 1, 1000)

        res_entries = []
        result_list = []

        # up two ~ 1,000 entries allowed per batch according to
        # https://www.dropbox.com/developers/reference/data-ingress-guide
        for chunk in chunks(entries, n=batch_size):

            arg = [files.DeleteArg(e[0], e[1]) for e in chunk]
            res = self.dbx.files_delete_batch(arg)

            if res.is_complete():
                batch_res = res.get_complete()
                res_entries.extend(batch_res.entries)

            elif res.is_async_job_id():
                async_job_id = res.get_async_job_id()

                time.sleep(1.0)
                res = self.dbx.files_delete_batch_check(async_job_id)

                check_interval = round(len(chunk) / 100, 1)

                while res.is_in_progress():
                    time.sleep(check_interval)
                    res = self.dbx.files_delete_batch_check(async_job_id)

                if res.is_complete():
                    batch_res = res.get_complete()
                    res_entries.extend(batch_res.entries)

                elif res.is_failed():
                    error = res.get_failed()
                    if error.is_too_many_write_operations():
                        title = 'Could not delete items'
                        text = ('There are too many write operations happening in your '
                                'Dropbox. Please try again later.')
                        raise SyncError(title, text)

        for i, entry in enumerate(res_entries):
            if entry.is_success():
                result_list.append(entry.get_success().metadata)
            elif entry.is_failure():
                exc = exceptions.ApiError(
                    error=entry.get_failure(),
                    user_message_text=None,
                    user_message_locale=None,
                    request_id=None,
                )
                sync_err = dropbox_to_maestral_error(exc, dbx_path=entries[i][0])
                result_list.append(sync_err)

        return result_list

    @to_maestral_error(dbx_path_arg=2)
    def move(self, dbx_path, new_path, **kwargs):
        """
        Moves / renames files or folders on Dropbox.

        :param str dbx_path: Path to file/folder on Dropbox.
        :param str new_path: New path on Dropbox to move to.
        :param kwargs: Keyword arguments for Dropbox SDK files_move_v2.
        :returns: Metadata of moved item.
        :rtype: :class:`files.Metadata`
        """
        res = self.dbx.files_move_v2(
            dbx_path,
            new_path,
            allow_shared_folder=True,
            allow_ownership_transfer=True,
            **kwargs
        )
        md = res.metadata

        return md

    @to_maestral_error(dbx_path_arg=1)
    def make_dir(self, dbx_path, **kwargs):
        """
        Creates a folder on Dropbox.

        :param str dbx_path: Path of Dropbox folder.
        :param kwargs: Keyword arguments for Dropbox SDK files_create_folder_v2.
        :returns: Metadata of created folder.
        :rtype: :class:`files.FolderMetadata`
        """
        res = self.dbx.files_create_folder_v2(dbx_path, **kwargs)
        md = res.metadata

        return md

    @to_maestral_error()
    def make_dir_batch(self, dbx_paths, batch_size=900, **kwargs):
        """
        Creates multiple folders on Dropbox in a batch job.

        :param list[str] dbx_paths: List of dropbox folder paths.
        :param int batch_size: Number of folders to create in each batch. Dropbox allows
            batches of up to 1,000 folders. Larger values will be capped automatically.
        :param kwargs: Keyword arguments for Dropbox SDK files_create_folder_batch.
        :returns: List of Metadata for created folders or SyncError for failures. Entries
            will be in the same order as given paths.
        :rtype: list
        """
        batch_size = clamp(batch_size, 1, 1000)

        entries = []
        result_list = []

        # up two ~ 1,000 entries allowed per batch according to
        # https://www.dropbox.com/developers/reference/data-ingress-guide
        for chunk in chunks(dbx_paths, n=batch_size):
            res = self.dbx.files_create_folder_batch(chunk, **kwargs)
            if res.is_complete():
                batch_res = res.get_complete()
                entries.extend(batch_res.entries)
            elif res.is_async_job_id():
                async_job_id = res.get_async_job_id()

                time.sleep(1.0)
                res = self.dbx.files_create_folder_batch_check(async_job_id)

                check_interval = round(len(chunk) / 100, 1)

                while res.is_in_progress():
                    time.sleep(check_interval)
                    res = self.dbx.files_create_folder_batch_check(async_job_id)

                if res.is_complete():
                    batch_res = res.get_complete()
                    entries.extend(batch_res.entries)

                elif res.is_failed():
                    error = res.get_failed()
                    if error.is_too_many_files():
                        res_list = self.make_dir_batch(
                            chunk,
                            batch_size=round(batch_size / 2),
                            **kwargs
                        )
                        result_list.extend(res_list)

        for i, entry in enumerate(entries):
            if entry.is_success():
                result_list.append(entry.get_success().metadata)
            elif entry.is_failure():
                exc = exceptions.ApiError(
                    error=entry.get_failure(),
                    user_message_text=None,
                    user_message_locale=None,
                    request_id=None,
                )
                sync_err = dropbox_to_maestral_error(exc, dbx_path=dbx_paths[i])
                result_list.append(sync_err)

        return result_list

    @to_maestral_error(dbx_path_arg=1)
    def get_latest_cursor(self, dbx_path, include_non_downloadable_files=False, **kwargs):
        """
        Gets the latest cursor for the given folder and subfolders.

        :param str dbx_path: Path of folder on Dropbox.
        :param bool include_non_downloadable_files: If ``True``, files that cannot be
            downloaded (at the moment only G-suite files on Dropbox) will be included.
        :param kwargs: Other keyword arguments for Dropbox SDK files_list_folder.
        :returns: The latest cursor representing a state of a folder and its subfolders.
        :rtype: str
        """

        dbx_path = '' if dbx_path == '/' else dbx_path

        res = self.dbx.files_list_folder_get_latest_cursor(
            dbx_path,
            include_non_downloadable_files=include_non_downloadable_files,
            recursive=True,
            **kwargs,
        )

        return res.cursor

    @to_maestral_error(dbx_path_arg=1)
    def list_folder(self, dbx_path, max_retries_on_timeout=4,
                    include_non_downloadable_files=False, **kwargs):
        """
        Lists the contents of a folder on Dropbox.

        :param str dbx_path: Path of folder on Dropbox.
        :param int max_retries_on_timeout: Number of times to try again if Dropbox servers
            don't respond within the timeout. Occasional timeouts may occur for very large
            Dropbox folders.
        :param bool include_non_downloadable_files: If ``True``, files that cannot be
            downloaded (at the moment only G-suite files on Dropbox) will be included.
        :param kwargs: Other keyword arguments for Dropbox SDK files_list_folder.
        :returns: Content of given folder.
        :rtype: :class:`files.ListFolderResult`
        """

        dbx_path = '' if dbx_path == '/' else dbx_path

        results = []

        res = self.dbx.files_list_folder(
            dbx_path,
            include_non_downloadable_files=include_non_downloadable_files,
            **kwargs
        )
        results.append(res)

        idx = 0

        while results[-1].has_more:

            idx += len(results[-1].entries)
            logger.info(f'Indexing {idx}...')

            attempt = 0

            while True:
                try:
                    more_results = self.dbx.files_list_folder_continue(results[-1].cursor)
                    results.append(more_results)
                    break
                except requests.exceptions.ReadTimeout:
                    attempt += 1
                    if attempt <= max_retries_on_timeout:
                        time.sleep(5.0)
                    else:
                        raise

        return self.flatten_results(results)

    @staticmethod
    def flatten_results(results):
        """
        Flattens a list of :class:`files.ListFolderResult` instances to a single
        instance with the cursor of the last entry in the list.

        :param list results: List of :class:`files.ListFolderResult` instances.
        :returns: Flattened list folder result.
        :rtype: :class:`files.ListFolderResult`
        """
        entries_all = []
        for result in results:
            entries_all += result.entries

        results_flattened = files.ListFolderResult(
            entries=entries_all, cursor=results[-1].cursor, has_more=False
        )

        return results_flattened

    @to_maestral_error()
    def wait_for_remote_changes(self, last_cursor, timeout=40):
        """
        Waits for remote changes since ``last_cursor``. Call this method after
        starting the Dropbox client and periodically to get the latest updates.

        :param str last_cursor: Last to cursor to compare for changes.
        :param int timeout: Seconds to wait until timeout. Must be between 30 and 480.
        :returns: ``True`` if changes are available, ``False`` otherwise.
        :rtype: bool
        """

        if not 30 <= timeout <= 480:
            raise ValueError('Timeout must be in range [30, 480]')

        # honour last request to back off
        time_to_backoff = max(self._backoff_until - time.time(), 0)
        time.sleep(time_to_backoff)

        result = self.dbx.files_list_folder_longpoll(last_cursor, timeout=timeout)

        # keep track of last longpoll, back off if requested by SDK
        if result.backoff:
            self._backoff_until = time.time() + result.backoff + 5.0
        else:
            self._backoff_until = 0

        return result.changes

    @to_maestral_error()
    def list_remote_changes(self, last_cursor):
        """
        Lists changes to remote Dropbox since ``last_cursor``. Call this after
        :meth:`wait_for_remote_changes` returns ``True``.

        :param str last_cursor: Last to cursor to compare for changes.
        :returns: Remote changes since given cursor.
        :rtype: :class:`files.ListFolderResult`
        """

        results = [self.dbx.files_list_folder_continue(last_cursor)]

        while results[-1].has_more:
            more_results = self.dbx.files_list_folder_continue(results[-1].cursor)
            results.append(more_results)

        # combine all results into one
        results = self.flatten_results(results)

        return results


def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)
