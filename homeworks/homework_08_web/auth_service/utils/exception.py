class ApiException(Exception):

    def __init__(self, code: int, name: str, description: str) -> None:
        self.code = code
        self.name = name
        self.description = description
