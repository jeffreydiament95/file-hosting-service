import pytest
from FileServer import *

def test_file_search():
    file_server = FileServer(files={})

    for i in range(1,7):
        file_server.file_upload(f"file-{i}.txt", i*11)

    results = file_server.file_search("blah")
    assert len(results) == 0

    results = file_server.file_search("file")
    assert results == ["file-6.txt", "file-5.txt", "file-4.txt"]

    # alphabetically should come first
    file_server.file_upload(f"filA-6.txt", 66)
    results = file_server.file_search("fil")
    assert results == ["filA-6.txt", "file-6.txt", "file-5.txt"]




