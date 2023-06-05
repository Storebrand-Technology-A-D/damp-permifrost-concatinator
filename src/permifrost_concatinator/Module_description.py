import logging


class Module_description:
    def __init__(self, type):
        self.type = type
        self.entities = []
        self.count = 0
        self.description = {}
        self.log = logging.getLogger(__name__)
        self.log.info(f"Creating {self.type} description")

    def gather_description(self, module):
        self.log.info(f"Gathering {self.type} description")
        self.count = len(module.spesification)
        self.entities = list(module.spesification.keys())
        return self

    def return_description(self):
        self.log.info(f"Returning {self.type} description")
        self.description["count"] = self.count
        self.description["entities"] = self.entities
        return self.description
