
import re
from enum import Enum
from . import Data
from .matching import MatchAnyString
from .matching import CaptureString 
from .matching import MatchUntilEnd
from .matching import MatchStringWithValue
from .matching import MatchDataWithName 
from .matching import CaptureData 

class Result(Enum):
    Ok = 1
    Fail = 2

Res = 0
Con = 1
Val = 2

def matcher(input):
    # TODO
    # TODO make sure * is always last

    def body(input):

        l_paren_result = l_paren(input)

        if l_paren_result[Res] is Result.Fail:
            return (Result.Fail, input)

        ret = []

        r_paren_result = r_paren(l_paren_result[Con])

        con = l_paren_result[Con]

        while r_paren_result[Res] is not Result.Ok:
            data_result = matcher(con)

            if data_result[Res] is Result.Fail:
                raise Exception("Found invalid input inside data body parser")
            
            con = data_result[Con]
            ret.append(data_result[Val])
            r_paren_result = r_paren(con)

            if r_paren_result[Res] is Result.Fail:
                comma_result = comma(con)
                if comma_result[Res] is Result.Fail:
                    raise Exception("Expected comma inside data body parser")
                con = comma_result[Con]

        return (Result.Ok, r_paren_result[Con], ret)

    ret = Data()

    dot_result = dot(input)

    if dot_result[Res] is Result.Ok:
        pass

    var_result = variable(input)


    if var_result[Res] is Result.Ok:
        ret.name = var_result[Val]
        body_result = body(var_result[Con])

        if body_result[Res] is Result.Ok:
            ret.args = body_result[Val]
            return (Result.Ok, body_result[Con], ret)
        elif body_result[Res] is Result.Fail:
            return (Result.Fail, input)
        else:
            raise Exception("impossible")
        
    elif var_result[Res] is Result.Fail:
        sym_result = symbol(input)
        
        if sym_result[Res] is Result.Ok:
            ret.name = sym_result[Val]
            body_result = body(sym_result[Con])

            if body_result[Res] is Result.Ok:
                ret.args = body_result[Val]
                return (Result.Ok, body_result[Con], ret)
            elif body_result[Res] is Result.Fail:
                return (Result.Fail, input)
            else:
                raise Exception("impossible")
        elif sym_result[Res] is Result.Fail:
            return (Result.Fail, input)
        else:
            raise Exception("impossible")
    else:
        raise Exception("impossible")
    
def dot(input):
    m = re.match("\s*\.(.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

def star(input):
    m = re.match("\s*\*(.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

def symbol(input):
    m = re.match("\s*([a-z0-9]\w*)(.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[1], gs[0])

def variable(input):
    m = re.match("\s*([A-Z]\w*)(.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[1], gs[0])

def comma(input):
    m = re.match("\s*,(.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

def l_paren(input):
    m = re.match("\s*\((.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

def r_paren(input):
    m = re.match("\s*\)(.*$)", input)
    if m is None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

# . -> match any one string
# * -> match any number of strings or data
# x -> match 'x'
# X -> match string with capture name X
# x() -> match data { name: x, args:[] } 
# X() -> match data { name: ?, args:[] } and capture with name X
# X(*) -> match data { name: ?, args:[?]}
# x(y(z, h(), *)) -> match data { name: x, args:[ data { name: y, args: ['z', data { name: h, args:[] }]}, ... ]}
# x(), y(), z() -> match [data { name: x, args:[]}, data { name: y, args:[]}, data { name: z, args:[]} ]
def parse_matcher(str):
    pass

# blah -> "blah"
# x(blah)  -> data { name: x, args: ["blah"]}
# x(y()) -> data { name: x, args: [data{name:y, args:[]}]}
def parse_data(input):
    def helper(input):
        def body(input):

            l_paren_result = l_paren(input)

            if l_paren_result[Res] is Result.Fail:
                return (Result.Fail, input)

            ret = []

            r_paren_result = r_paren(l_paren_result[Con])

            con = l_paren_result[Con]

            while r_paren_result[Res] is not Result.Ok:
                data_result = helper(con)

                if data_result[Res] is Result.Fail:
                    raise Exception("Found invalid input inside data body parser")
                
                con = data_result[Con]
                ret.append(data_result[Val])
                r_paren_result = r_paren(con)

                if r_paren_result[Res] is Result.Fail:
                    comma_result = comma(con)
                    if comma_result[Res] is Result.Fail:
                        raise Exception("Expected comma inside data body parser")
                    con = comma_result[Con]

            return (Result.Ok, r_paren_result[Con], ret)

        ret = Data()

        sym_result = symbol(input)
        
        if sym_result[Res] is Result.Ok:
            ret.name = sym_result[Val]
            body_result = body(sym_result[Con])

            if body_result[Res] is Result.Ok:
                ret.args = body_result[Val]
                return (Result.Ok, body_result[Con], ret)
            elif body_result[Res] is Result.Fail:
                return (Result.Ok, sym_result[Con], sym_result[Val])
            else:
                raise Exception("impossible")
        elif sym_result[Res] is Result.Fail:
            return (Result.Fail, input)
        else:
            raise Exception("impossible")

    helper_result = helper(input)
    if helper_result[Res] is Result.Ok and helper_result[Con] == '':
        return helper_result[Val]
    elif helper_result[Res] is Result.Ok:
        raise Exception(f"Data parser did not parse entire input: {helper_result[Con]}")
    else:
        raise Exception("Failure to parse data")