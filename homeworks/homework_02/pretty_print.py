class IncorrectFormat(Exception):
    pass


class PrettyPrint:
    def __init__(self, handler, text):
        self.handler = handler
        self.text = text

    def pretty_print(self):
        self.handler.pretty_print(self.text)
