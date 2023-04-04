import pytest
from FileServer import *

def test_file_upload():
    file_server = FileServer(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11

    file_server.file_upload(file_name_1, file_size_1)
    assert file_server.file_exists(file_name_1)
    with pytest.raises(RuntimeError):
        file_server.file_upload(file_name_1, file_size_1)


def test_file_get():
    file_server = FileServer(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11
    file_name_2 = "file-2.txt"

    file_server.file_upload(file_name_1, file_size_1)
    assert file_server.file_get(file_name_1) == 11
    assert not file_server.file_get(file_name_2)

def test_file_copy():
    file_server = FileServer(files={})

    file_name_1 = "file-1.txt"
    file_size_1 = 11
    file_name_2 = "file-2.txt"
    file_size_2 = 22
    file_name_3 = "file-3.txt"
    file_size_3 = 33

    # If the source file doesn’t exist, throws a runtime exception
    with pytest.raises(RuntimeError):
        file_server.file_copy(file_name_1, file_name_3)

    # Copy source file to a new location
    file_server.file_upload(file_name_1, file_size_1)
    file_server.file_upload(file_name_2, file_size_2)
    file_server.file_copy(file_name_1, file_name_3)
    assert file_server.file_get(file_name_3) == file_size_1
    assert not file_server.file_exists(file_name_1)

    # If the destination file already exists, overwrite existing file
    file_server = FileServer(files={})
    file_server.file_upload(file_name_1, file_size_1)
    file_server.file_upload(file_name_2, file_size_2)
    file_server.file_copy(file_name_1, file_name_2)
    assert file_server.file_get(file_name_2) == file_size_1
    assert not file_server.file_exists(file_name_1)




