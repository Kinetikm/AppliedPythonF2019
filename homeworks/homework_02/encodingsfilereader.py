from exceptions import FileNotFound


class EncodingsFileReader:
    __encodings = ['cp1251', 'utf-16', 'utf-8']

    def __init__(self, file_name):
        try:
            for i in EncodingsFileReader.__encodings:
                try:
                    with open(file_name, encoding=i) as file:
                        self.__output_str = file.read()
                        self.encoding = i
                except (UnicodeDecodeError, UnicodeError):
                    pass
        except (FileNotFoundError):
            raise FileNotFound()

    @property
    def output_string(self):
        return self.__output_str
