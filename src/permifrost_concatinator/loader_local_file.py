import logging
import os
import json
import yaml


class Local_file_loader:
    def __init__(self, format) -> None:
        self.format = format
        self.log = logging.getLogger(__name__)
        self.log.info(f"Creating Local file loader for {format}")

    def load(self, key):
        self.log.info(f"Loading {self.format} file from {key}")
        if self.format == "json":
            self.log.debug("Detecting Json format to be loaded")
            file = self.__json(key)

        elif self.format == "yaml":
            self.log.debug("Detecting Yaml format to be loaded")
            file = self.__yaml(key)

        self.log.info(f"File sucsessfully read")
        return file

    def __json(self, key):
        self.log.debug(f"Json loader recived {key}")
        with open(key, "r") as file:
            file = json.load(file)
            self.log.debug(f"managed to load file")
        return file

    def __yaml(self, key):
        self.log.debug(f"Yaml loader recived {key}")
        try:
            with open(key, "r") as file:
                file = yaml.safe_load(file)
                self.log.debug(f"Managed to read files")
        except yaml.YAMLError:
            self.log.error(f"File not yaml: {file}")
            raise Exception("File not yaml")
        return file
