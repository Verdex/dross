
import itertools

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

    def __init__(self, matchers):
        self.matchers = matchers

    def match_all(self, data):
        # type(data) is str
        # type(data) is Data
        # type(data) is array of Data|str?
        pass
    
    def match(self, data):
        # data : Data | str | [(Data|str)]
        # ret : (bool, Match)
        # matchers has to be length 1?
        pass

    def match_first(self, data):
        pass

    def match_exact(self, data):
        pass

class MatchAnyString: # dot
    def match(self, data):
        if type(data) is str:
            return Match(data)
        else:
            return Match()

class CaptureString:
    def __init__(self, capture_name):
        self.capture_name = capture_name
    
    def match(self, data):
        if type(data) is str:
            return Match(data, {self.capture_name: data})
        else:
            return Match()

class MatchUntilEnd: # star
    pass

class MatchStringWithValue:
    def __init__(self, value):
        self.value = value
    
    def match(self, data):
        if type(data) is str and data == self.value:
            return Match(data)
        else:
            return Match()

class MatchDataWithName:
    def __init__(self, name, sub_matchers = []):
        self.target_name = name
        self.sub_matchers = sub_matchers

    def match(self, data):
        if type(data) is Data and data.name == self.target_name:
            matches = []
            for (m, d) in itertools.zip_longest(self.sub_matchers, data.args):
                if m is None and d is not None:
                    return Match()
                elif type(m) is MatchUntilEnd:
                    all_captures = merge_captures(map(lambda x: x.captures, matches))
                    return Match(data, all_captures)
                elif m is not None and d is None:
                    return Match()
                else:
                    r = m.match(d)
                    if r.name is None:
                        return Match()
                    else:
                        matches.append(r)
            
            all_captures = merge_captures(map(lambda x: x.captures, matches))
            return Match(data, all_captures)
        else:
            return Match()

class CaptureData:
    def __init__(self, capture_name, sub_matchers = []):
        self.capture_name = capture_name
        self.sub_matchers = sub_matchers

    def match(self, data):
        if type(data) is Data:
            matches = [{self.capture_name: data}]
            for (m, d) in itertools.zip_longest(self.sub_matchers, data.args):
                if m is None and d is not None:
                    return Match()
                elif type(m) is MatchUntilEnd:
                    all_captures = merge_captures(map(lambda x: x.captures, matches))
                    return Match(data, all_captures)
                elif m is not None and d is None:
                    return Match()
                else:
                    r = m.match(d)
                    if r.name is None:
                        return Match()
                    else:
                        matches.append(r)
            
            all_captures = merge_captures(map(lambda x: x.captures, matches))
            return Match(data, all_captures)
        else:
            return Match()

class Match:
    def __init__(self, match = None, captures = {}):
        self.match = match
        self.captures = captures

def merge_captures(matches):
    ret = {}

    for match in matches:
        for (key, value) in match.items():
            if key in ret:
                raise Exception(f'Found already existing key: {key}')
            ret[key] = value
    
    return ret

    