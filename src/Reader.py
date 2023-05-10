import os
import yaml


class Reader:
    def __init__(self):
        self.files = []

    """
    This class is responsible for reading Pemifrost files from a directory.
    """

    def read_dir(self, path):
        """
        This method reads all files from a directory and returns a list of files.
        """
        try:
            self.files = [
                os.path.join(path, f)
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]
        except FileNotFoundError:
            raise Exception("Directory not found")
        return self.files

    def get_file(self, spec_file):
        """
        This method reads a file and returns a dictionary.
        """

        try:
            with open(spec_file, "r") as file_to_read:
                try:
                    file = yaml.safe_load(file_to_read)
                except yaml.YAMLError:
                    raise Exception("File not yaml")
        except FileNotFoundError:
            raise Exception("File not found")
        return file
