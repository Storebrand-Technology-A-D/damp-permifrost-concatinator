import logging


class SpecVerification:
    def __init__(self, spec):
        self.spec = spec
        self.log = logging.getLogger(__name__)
        self.log.info("Spec verification initialized")
