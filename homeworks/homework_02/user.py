class User:
    def __init__(self, id):
        self.id = id
        self.posted = set()
        self.subscriptions = set()

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == self.other
