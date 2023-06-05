import logging


class Yaml_file_Writer:
    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.log.info("Yaml file Writer initialized")

    def write(self, file_name, content):
        try:
            with open(file_name, "w") as file:
                file.write(content)
            self.log.debug("File written successfully in w mode")
        except:
            with open(file_name, "x") as file:
                file.write(content)
            self.log.debug("File written successfully in x mode")
        return True
