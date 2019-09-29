
class TableReader():

    def __init__(self, filename: str) -> None:
        self.known_encodings = ['utf-8', 'utf-16', 'cp1251']
        self.filename = filename

        # кодировка, в которой был файл
        self.encoding = None

    def read(self):
        for enc in self.known_encodings:
            try:
                with open(file=self.filename, encoding=enc) as file:
                    lines = file.read()
                    self.encoding = enc
                    return lines
            except (SyntaxError, AttributeError, UnicodeDecodeError, UnicodeError, TypeError):
                continue

        return None
