from .Base_module import Base_Module
import logging


class Warehouses_Module(Base_Module):
    def __init__(self):
        self.spesification = {}
        self.type = "Warehouse"
        self.log = logging.getLogger(__name__)
