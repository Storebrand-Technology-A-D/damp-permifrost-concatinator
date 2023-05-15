from src.Module_description import Module_description
class Base_Module:
    def __init__(self):
        self.spesification = {}
        self.type = "Entity"

    def add_entities(self, entities):
        for entity in entities:
            self.spesification.update(entity)

    def get_entities(self, entity):
        if self.is_entity(entity):
            return self.spesification[entity]
        else:
            raise Exception(f"{self.type} not found")

    def is_entity(self, entity):
        return entity in self.spesification
    
    def describe(self):
        description = Module_description(self.type)
        description.gather_description(self)
        return description