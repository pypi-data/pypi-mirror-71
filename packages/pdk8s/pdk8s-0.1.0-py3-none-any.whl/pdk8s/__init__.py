import yaml

__version__ = "0.1.0"

class Chart:
    def __init__(self, context, ns: str):
        self.context = context
        self.ns = ns

