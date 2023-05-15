class Module_description:
    def __init__(self, type):
        self.type = ""
        self.entities = []
        self.count = 0
        self.description = {}

    def gather_description(self, module):
        self.count = len(module.spesification)
        self.entities = list(module.spesification.keys())
        return self
    
    def return_description(self):
        self.description["count"] = self.count
        self.description["entities"] = self.entities
        return self.description