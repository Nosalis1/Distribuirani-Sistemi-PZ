import os


class DistributedFile:
    def __init__(self, file_name):
        self.file_name = os.path.basename(file_name)
        self.file_size = os.path.getsize(file_name)
        self.file_last_modified = os.path.getmtime(file_name)
        pass

    def json(self):
        return {
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_last_modified': self.file_last_modified
        }
        pass

    def __repr__(self):
        return f"""
        file_name: {self.file_name}\n
        file_size: {self.file_size}\n
        file_last_modified: {self.file_last_modified}\n
        """

    def __str__(self):
        return self.file_name


def load_shared_directory(path):
    files = []
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            files.append(DistributedFile(file_path))
    return files
