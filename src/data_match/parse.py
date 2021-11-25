
import re
from enum import Enum

class Result(Enum):
    Ok = 1
    Fail = 2
    Fatal = 3

def data(input):

    def body(input):

        def comma(input):
            m = re.match("\s*,(.*$)", input)
            if m == None:
                return (Result.Fail, input)
            else:
                gs = m.groups()
                return (Result.Ok, gs[0])

        def l_paren(input):
            m = re.match("\s*\((.*$)", input)
            if m == None:
                return (Result.Fail, input)
            else:
                gs = m.groups()
                return (Result.Ok, gs[0])

        def r_paren(input):
            m = re.match("\s*\)(.*$)", input)
            if m == None:
                return (Result.Fail, input)
            else:
                gs = m.groups()
                return (Result.Ok, gs[0])

        return (Result.Ok, input, '')

    (var_res, cont, name) = variable(input)

    if var_res == Result.Fatal:
        raise Exception("Fatal variable parse")
    
    else if var_res == Result.Ok:
        
    else if var_res == Result.Fail:
        (sym_res, cont, name) = symbol(input)
        if var_res == Result.Fatal:
            raise Exception("Fatal symbol parse")
        
        else if var_res == Result.Ok:

    
    return (Result.Ok, '')

def dot(input):
    m = re.match("\s*\.(.*$)", input)
    if m == None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

def star(input):
    m = re.match("\s*\*(.*$)", input)
    if m == None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[0])

def symbol(input):
    m = re.match("\s*([a-z]\w*)(.*$)", input)
    if m == None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[1], gs[0])

def variable(input):
    m = re.match("\s*([A-Z]\w*)(.*$)", input)
    if m == None:
        return (Result.Fail, input)
    else:
        gs = m.groups()
        return (Result.Ok, gs[1], gs[0])

# . -> match any one string
# * -> match any number of strings or data
# x -> match 'x'
# X -> match string with capture name X
# x() -> match data { name: x, args:[] } 
# X() -> match data { name: ?, args:[] } and capture with name X
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