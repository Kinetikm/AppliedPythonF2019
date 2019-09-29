class PrettyPrint:

    __slots__ = ["handler"]

    def __init__(self, handler):
        self.handler = handler

    def pretty_print(self):
        self.handler.pretty_print()
