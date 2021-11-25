
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
    pass

    def match_all(self, data):
        # type(data) is str
        # type(data) is Data
        pass
    
    def match_total(self, data):
        pass

# . -> match any string
# x -> match 'x'
# x() -> match data { name: x, args:[] }
# X() -> match data { name: ?, args:[] }
# X(*) -> match data { name: ?, args:[?]}
# x(y(z, h(), *)) -> match data { name: x, args:[ data { name: y, args: ['z', data { name: h, args:[] }]}, ... ]}
# x(), y(), z() -> match [data { name: x, args:[]}, data { name: y, args:[]}, data { name: z, args:[]} ]
# * -> match any number of things
def parse_matcher(str):
    pass

# blah -> "blah"
# x(blah)  -> data { name: x, args: ["blah"]}
# x(y()) -> data { name: x, args: [data{name:y, args:[]}]}
def parse_data(str):
    pass