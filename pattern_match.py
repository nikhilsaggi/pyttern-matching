SUPPORTED_TYPES = [int, bool, str, list]

class Infix:
    def __init__(self, function):
        self.function = function
    def __ror__(self, other):
        return Infix(lambda x, self=self, other=other: self.function(other, x))
    def __or__(self, other):
        return self.function(other)

### PATTERN MATCH IMPLEMENTATION ###

def unroll_types(e, pattern):
    context = {}

    if type(e) != list or len(e) < 2:
        return False, context
    if type(pattern) == tuple: # TODO: define cons operator instead of tuple
        if pattern[0].get_type() == type(e[0]) and pattern[1].get_type() == type(e[1:]):
            context[pattern[0].get_name()] = e[0]
            context[pattern[1].get_name()] = e[1:]
            return True, context

    return False, context

def pattern_match(e, patterns):
    for pattern, command in patterns:
        types_match, context = unroll_types(e, pattern)
        if e == pattern or types_match:
            if type(pattern) == tuple:
                if type(command) == str and command.startswith('recurse'):
                    return pattern_match(context[command.split(' ')[1]], patterns)
            else:
                return command
    return False

### DATA STRUCTURES ###

class Cons:
    def __init__(self, l):
        if len(l) == 0:
            self._data = (None, [])
        else:
            self._data = (l[0], l[1:])

    def hd(self):
        return self._data[0]

    def tl(self):
        return self._data[1]

class Variable:
    def __init__(self, name, t):
        if t not in SUPPORTED_TYPES:
            raise Exception(f"Type not supported; please use one of {SUPPORTED_TYPES}")
        if type(name) != str:
            raise Exception(f"Name of Variable should be type string")
        self._name = name
        self._type = t

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

### OPERATIONS ###

def search(l, el):
    return pattern_match(l, [
        ([], False),
        ([el], True),
        ([el] + l[1:], True),
        ((Variable("h", int), Variable("t", list)), "recurse t") # TODO: define cons operator instead of tuple
    ])