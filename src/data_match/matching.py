
class Data:
    def __init__(self):
        self.name = ''
        self.args = []

    def serialize(self):
        args = []
        for value in self.args:
            if type(value) is Data:
                args.append(value.serialize())
            else:
                args.append(value)

        return f'{self.name}({",".join(args)})'


class Matcher:

    def match_all(self, data):
        # type(data) is str
        # type(data) is Data
        pass
    
    def match_total(self, data):
        pass
