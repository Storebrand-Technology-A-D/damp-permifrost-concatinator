import logging
from src.Module_description import Module_description


class Base_Module:
    def __init__(self):
        self.spesification = {}
        self.type = "Entity"
        self.log = logging.getLogger(__name__)

    def add_entities(self, entities):
        self.log.debug(f"Adding {self.type}s: {entities}")
        self.log.debug(f"Current {self.type}s: {self.spesification}")
        for entity in entities:
            self.spesification.update(entity)

        self.log.debug(f"New {self.type}s: {self.spesification}")
        self.log.info(f"{self.type}s added to spec")

    def get_entities(self, entity):
        self.log.debug(f"Getting {self.type}s: {entity}")
        self.log.info(f"{self.type}s retrieved from spec")

        if self.is_entity(entity):
            return self.spesification[entity]
        else:
            self.log.error(f"{self.type} not found")
            raise Exception(f"{self.type} not found")

    def is_entity(self, entity):
        self.log.debug(f"Checking if {self.type} exists: {entity}")
        return entity in self.spesification

    def describe(self):
        self.log.info(f"Describing {self.type}")
        description = Module_description(self.type)
        description.gather_description(self)
        self.log.info(f"{self.type} described")
        self.log.debug(f"{self.type} description: {description}")
        return description
