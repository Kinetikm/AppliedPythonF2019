class Post:
    def __init__(self, id):
        self.id = id
        self.read = set()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == self.other
