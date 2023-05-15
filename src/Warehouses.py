from src.Module_description import Module_description
class Warehouses_Module:
    def __init__(self):
        self.spesification = {}

    def add_entities(self, warehouses):
        for warehouse in warehouses:
            self.spesification.update(warehouse)

    def get_entitiy(self, warehouse):
        if warehouse not in self.spesification:
            raise Exception("Warehouse not found")
        return self.spesification[warehouse]

    def is_entity(self, warehouse):
        return warehouse in self.spesification

    def describe(self):
        description = Module_description("warehouses")
        description.gather_description(self)
        return description
