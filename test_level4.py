import pytest
from FileServer import *


def test_rollback():
    file_server = FileServerTimestamp(files={})
    file_server.file_upload_at(1, "file-1.txt", 11, 5)
    file_server.file_upload_at(2, "file-2.txt", 22, 5)
    file_server.file_upload_at(3, "file-3.txt", 33, 5)
    file_server.file_upload_at(4, "file-4.txt", 44, 5)
    file_server.file_upload_at(5, "file-5.txt", 55, 5)
    file_server.file_upload_at(6, "file-6.txt", 66, 5)

    current_timestamp = 8
    assert not file_server.file_exists_at(current_timestamp, "file-1.txt")
    assert not file_server.file_exists_at(current_timestamp, "file-2.txt")
    assert file_server.file_exists_at(current_timestamp, "file-3.txt")
    assert file_server.file_exists_at(current_timestamp, "file-4.txt")
    assert file_server.file_exists_at(current_timestamp, "file-5.txt")
    assert file_server.file_exists_at(current_timestamp, "file-6.txt")

    print(f"initial configuration:\n{file_server}")
    rollback_timestamp = 4
    file_server.rollback(rollback_timestamp)
    print(f"after rollback:\n{file_server}")

    assert file_server.file_exists_at(rollback_timestamp, "file-1.txt")
    assert file_server.file_exists_at(rollback_timestamp, "file-2.txt")
    assert file_server.file_exists_at(rollback_timestamp, "file-3.txt")
    assert file_server.file_exists_at(rollback_timestamp, "file-4.txt")
    assert not file_server.file_exists_at(rollback_timestamp, "file-5.txt")
    assert not file_server.file_exists_at(rollback_timestamp, "file-6.txt")

    # # check ttls are updated correctly
    # assert file_server.files["file-1.txt"].timestamp == rollback_timestamp and file_server.files[
    #     "file-1.txt"].ttl == 2
    # assert file_server.files["file-2.txt"].timestamp == rollback_timestamp and file_server.files[
    #     "file-2.txt"].ttl == 3
    # assert file_server.files["file-3.txt"].timestamp == rollback_timestamp and file_server.files[
    #     "file-3.txt"].ttl == 4
    # assert file_server.files["file-4.txt"].timestamp == rollback_timestamp and file_server.files[
    #     "file-4.txt"].ttl == 5
