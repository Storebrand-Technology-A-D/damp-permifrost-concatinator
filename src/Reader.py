import os
import yaml
import logging


class Reader:
    def __init__(self):
        self.files = []
        self.log = logging.getLogger(__name__)
        self.log.info("Creating Reader")

    """
    This class is responsible for reading Pemifrost files from a directory.
    """

    def read_dir(self, path):
        """
        This method reads all files from a directory and returns a list of files.
        """
        self.log.info(f"Reading directory: {path}")
        try:
            self.files = [
                os.path.join(path, f)
                for f in os.listdir(path)
                if os.path.isfile(os.path.join(path, f))
            ]
            self.log.debug(f"Files read: {self.files}")
        except FileNotFoundError:
            self.log.error(f"Directory not found: {path}")
            raise Exception("Directory not found")
        self.log.info("Directory read")
        return self.files

    def get_file(self, spec_file):
        """
        This method reads a file and returns a dictionary.
        """
        self.log.info(f"Reading file: {spec_file}")
        try:
            with open(spec_file, "r") as file_to_read:
                try:
                    file = yaml.safe_load(file_to_read)
                    self.log.debug(f"File read: {file}")
                except yaml.YAMLError:
                    self.log.error(f"File not yaml: {spec_file}")
                    raise Exception("File not yaml")
        except FileNotFoundError:
            self.log.error(f"File not found: {spec_file}")
            raise Exception("File not found")
        self.log.info("File read")
        return file
