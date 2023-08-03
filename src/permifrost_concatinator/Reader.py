import os
import yaml
import logging

from .loader_local_file import Local_file_loader


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
            yaml = Local_file_loader("yaml")
            file = yaml.load(spec_file)
            self.log.debug(f"File read: {file}")

        except FileNotFoundError:
            self.log.error(f"File not found: {spec_file}")
            raise Exception("File not found")
        self.log.info("File read")
        return file
