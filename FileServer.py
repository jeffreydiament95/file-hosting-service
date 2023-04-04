class FileServer:
    def __init__(self, files={}):
        # dictionary with key as file name and value as File object
        self.files = files

    def __str__(self):
        output = ""
        for file in self.files:
            output += f"{self.files[file]}\n"
        return output

    def file_upload(self, file_name, size):
        if self.file_exists(file_name):
            raise RuntimeError(f"{file_name} already exists and cannot be added to the server.")
        else:
            file = File(size)
            self.files[file_name] = file

    def file_get(self, file_name):
        if self.file_exists(file_name):
            return self.files[file_name].size
        else:
            return None

    def file_copy(self, source, dest):
        if not self.file_exists(source):
            raise RuntimeError(f"{source} does not exist and thus cannot be copied.")

        elif self.file_exists(dest):
            # overwrite dest attributes with source data
            self.files[dest].size = self.files[source].size

            # delete original source file
            self.files.pop(source)

        else: # if not self.file_exists(dest)
            # create new dest file
            self.file_upload(dest, self.files[source].size)

            # delete original source file
            self.files.pop(source)

    def file_search(self, prefix):
        # matches[file_name] = size
        matches = []
        for file_name in self.files:
            if file_name.startswith(prefix):
                matches.append((file_name, self.files[file_name].size))

        matches.sort(key=lambda x: (-x[1], x[0]))

        # convert to array with only file names
        matches = [x[0] for x in matches]

        # return top 3 values
        return matches[:3]

    def file_exists(self, file_name):
        if file_name in self.files:
            return True
        else:
            return False

    # def __iter__(self):
    #     self.n = 0
    #     return self
    #
    # # iterates through file names
    # def __next__(self):
    #     if self.n < len(self.files):
    #         result = self.files[self.n][0]
    #         self.n += 1
    #         return result
    #     else:
    #         raise StopIteration

# not really any point in making this a subclass other than proof of concept
class FileServerTimestamp(FileServer):

    def file_upload_at(self, timestamp, file_name, size, ttl=None):
        if self.file_exists_at(timestamp, file_name):
            raise RuntimeError(f"{file_name} already exists and cannot be added to the server.")
        else:
            file = File(size, timestamp, ttl)
            self.files[file_name] = file

    def file_get_at(self, timestamp, file_name):
        if self.file_exists_at(timestamp, file_name):
            return self.files[file_name].size
        else:
            return None

    def file_copy_at(self, timestamp, source, dest):
        if not self.file_exists_at(timestamp, source):
            raise RuntimeError(f"{source} does not exist and thus cannot be copied.")

        elif self.file_exists_at(timestamp, dest):
            # overwrite dest attributes with source data
            self.files[dest].size = self.files[source].size
            self.files[dest].timestamp = self.files[source].timestamp
            self.files[dest].ttl = self.files[source].ttl

            # delete original source file
            self.files.pop(source)

        else:  # if not self.file_exists(dest)
            # create new dest file
            self.file_upload_at(timestamp, dest, self.files[source].size, self.files[source].ttl)

            # delete original source file
            self.files.pop(source)

    def file_search_at(self, timestamp, prefix):
        # matches[file_name] = size
        matches = []
        for file_name in self.files:
            file = self.files[file_name]
            # screen for files that aren't expired!
            if not file.ttl or (timestamp - file.timestamp) <= file.ttl:
                if file_name.startswith(prefix):
                    matches.append((file_name, self.files[file_name].size))

        matches.sort(key=lambda x: (-x[1], x[0]))

        # convert to array with only file names
        matches = [x[0] for x in matches]

        # return top 3 values
        return matches[:3]

    def file_exists_at(self, timestamp, file_name):
        if file_name in self.files:
            file = self.files[file_name]

            # infinite ttl
            if not file.ttl:
                return True

            # file does not exist yet!
            elif (timestamp - file.timestamp) < 0:
                return False

            # within finite ttl
            elif (timestamp - file.timestamp) <= file.ttl:
                return True

            # file used to exist but is now expired
            else:
                return False
        # file never existed
        else:
            return False

    def rollback(self, timestamp):
        files_to_delete = []

        for file_name in self.files:
            file = self.files[file_name]

            # infinite ttl
            if not file.ttl:
                file.timestamp = timestamp

            # delete files that have timestamp greater than rollback timestamp
            elif (timestamp - file.timestamp) < 0:
                files_to_delete.append(file_name)

            # rollback is within ttl, keep original values
            elif (timestamp - file.timestamp) <= file.ttl:
                pass

            # file used to exist but is still out of range, do nothing
            else:
                pass

        # avoid changing size of dictionary during loop iteration
        for file_name in files_to_delete:
            self.files.pop(file_name)
class File:
    def __init__(self, size, timestamp=None, ttl=None):
        self.size = size
        self.timestamp = timestamp
        self.ttl = ttl

    def __str__(self):
        return f"timestamp: {self.timestamp}, ttl: {self.ttl}"