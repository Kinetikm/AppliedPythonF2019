class InvalidFormat(Exception):
    def __str__(self):
        return "Формат не валиден"


class FileNotFound(Exception):
    def __str__(self):
        return "Данные не валидны"
