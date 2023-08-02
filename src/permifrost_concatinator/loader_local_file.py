import logging
import os
import json
import yaml

class Local_file_loader():
    def __init__(self, format) -> None:
        self.format = format

    def load(self, key):
        if self.format == "json":
            file = self.__json(key)

        elif self.format=="yaml":
            file = self.__yaml(key)
        return file

    def __json(self, key):
        with open(key, "r") as file:
            file = json.load(file)
        return file

    def __yaml(self, key):
        with open(key, "r") as file:
            file = yaml.safe_load(file)
        return file
