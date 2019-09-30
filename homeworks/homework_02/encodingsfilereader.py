from exceptions import FileNotFound


class EncodingsFileReader:
    __encodings = ['cp1251', 'utf-8', 'utf-16']

    def __init__(self, file_name):
        try:
            for i in EncodingsFileReader.__encodings:
                with open(file_name, 'rb') as file:
                    self.__output_str = file.read()
                    try:
                        self.__output_str.decode(i)
                        self.encoding = i
                    except UnicodeDecodeError:
                        self.encoding = "cp1251"
        except (FileNotFoundError):
            raise FileNotFound()

    @property
    def output_string(self):
        return self.__output_str
