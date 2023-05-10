class Spesification:
    """
    Class for holding onto a permifrost spessification as imported from a spec file.

    """

    def __init__(self, spec_file):
        self.spec_file = spec_file

    def identify(self):
        """
        Identify the modules in the spec file.
        """
        self.module_list = list(self.spec_file.keys())
        self.module_list.remove("version")
