import file_handler as fh


class Logics:
    def __init__(self):
        self.abfs = []

    def open_file_and_add_to_abfs(self, path_to_file):
        abf = fh.open_abf(path_to_file)
        self.abfs.append((path_to_file, abf))

    def open_abf(self, path_to_file):
        # list is empty, extract it
        if not self.abfs:
            self.open_file_and_add_to_abfs(path_to_file)
        else:
            file_names, _ = zip(*self.abfs)
            # file not already extracted
            if path_to_file not in file_names:
                self.open_file_and_add_to_abfs(path_to_file)

        # else do nothing
