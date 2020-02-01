class NameDict(dict):
    def __init__(self, items):
        super(NameDict, self).__init__({i.name: i for i in items})

    def __repr__(self):
        return str(set(self.values()))

    def __iter__(self):
        yield from self.values()
