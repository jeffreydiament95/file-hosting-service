import pytest
from FileServer import *


def test_file_upload_at():
    # test existing methods
    file_server_ts = FileServerTimestamp(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11

    file_server_ts.file_upload(file_name_1, file_size_1)
    assert file_server_ts.file_exists(file_name_1)
    with pytest.raises(RuntimeError):
        file_server_ts.file_upload(file_name_1, file_size_1)

    # test new methods
    file_server_ts = FileServerTimestamp(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11
    timestamp_1 = 1
    timestamp_2 = 2

    file_server_ts.file_upload_at(timestamp_1, file_name_1, file_size_1)
    assert file_server_ts.file_exists_at(timestamp_1, file_name_1)
    with pytest.raises(RuntimeError):
        file_server_ts.file_upload_at(timestamp_2, file_name_1, file_size_1)

    # test expiration
    file_server_ts = FileServerTimestamp(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11
    timestamp_1 = 1
    ttl_1 = 1
    timestamp_2 = 3
    timestamp_3 = 4

    file_server_ts.file_upload_at(timestamp_1, file_name_1, file_size_1, ttl_1)
    assert file_server_ts.file_exists_at(timestamp_1, file_name_1)
    assert not file_server_ts.file_exists_at(timestamp_2, file_name_1)
    file_server_ts.file_upload_at(timestamp_2, file_name_1, file_size_1, ttl_1)
    assert file_server_ts.file_exists_at(timestamp_3, file_name_1)


def test_file_get_at():
    file_name_1 = "file-1.txt"
    file_size_1 = 11
    file_name_2 = "file-2.txt"

    # no expiration
    file_server_ts = FileServerTimestamp(files={})

    file_server_ts.file_upload_at(1, file_name_1, file_size_1)
    assert file_server_ts.file_get_at(10, file_name_1) == 11
    assert not file_server_ts.file_get_at(10, file_name_2)

    # expiration
    file_server_ts = FileServerTimestamp(files={})

    file_server_ts.file_upload_at(1, file_name_1, file_size_1, 3)
    assert file_server_ts.file_get_at(2, file_name_1) == 11
    assert not file_server_ts.file_get_at(10, file_name_1)


def test_copy_file_at():
    file_server = FileServerTimestamp(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11
    file_name_2 = "file-2.txt"
    file_size_2 = 22
    file_name_3 = "file-3.txt"
    file_size_3 = 33

    # If the source file DNE, throws a runtime exception
    with pytest.raises(RuntimeError):
        file_server.file_copy_at(3, file_name_1, file_name_3)

    # If the source file is expired, throws a runtime exception
    file_server.file_upload_at(1, file_name_1, file_size_1, 10)
    with pytest.raises(RuntimeError):
        file_server.file_copy_at(13, file_name_1, file_name_3)

    # Copy source file to a new location
    file_server.file_upload_at(2, file_name_2, file_size_2, 10)
    file_server.file_copy_at(3, file_name_1, file_name_3)
    assert file_server.file_get_at(3, file_name_3) == file_size_1
    assert not file_server.file_exists_at(3, file_name_1)

    # If the destination file already exists, overwrite existing file
    file_server = FileServerTimestamp(files={})
    file_server.file_upload_at(1, file_name_1, file_size_1, 10)
    file_server.file_upload_at(1, file_name_2, file_size_2, 10)
    file_server.file_copy_at(3, file_name_1, file_name_2)
    assert file_server.file_get_at(3, file_name_2) == file_size_1
    assert not file_server.file_exists_at(3, file_name_1)

    # If the destination file is expired, overwrite old file
    file_server = FileServerTimestamp(files={})
    file_server.file_upload_at(1, file_name_1, file_size_1, 10)
    file_server.file_upload_at(1, file_name_2, file_size_2, 1)
    file_server.file_copy_at(5, file_name_1, file_name_2)
    assert file_server.file_get_at(5, file_name_2) == file_size_1
    assert not file_server.file_exists_at(5, file_name_1)

def test_file_search_at():
    file_server = FileServerTimestamp(files={})
    file_server.file_upload_at(5, "file-1.txt", 11, 2)
    file_server.file_upload_at(5, "file-2.txt", 22, 2)
    file_server.file_upload_at(5, "file-3.txt", 33, 2)
    file_server.file_upload_at(5, "filA-3.txt", 33, 2)


    file_server.file_upload_at(1, "file-4.txt", 44, 2)
    file_server.file_upload_at(1, "file-5.txt", 55, 2)
    file_server.file_upload_at(1, "file-6.txt", 66, 2)
    file_server.file_upload_at(1, "filA-6.txt", 66, 2)


    results = file_server.file_search_at(1,"blah")
    assert len(results) == 0

    results = file_server.file_search_at(2, "fil")
    assert results == ["filA-6.txt", "file-6.txt", "file-5.txt"]

    results = file_server.file_search_at(6, "fil")
    assert results == ["filA-3.txt", "file-3.txt", "file-2.txt"]