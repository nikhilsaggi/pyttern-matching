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
        # Cons
        h_checks = False # type of h in e=h::t matches type in specified pattern 
        t_checks = False # type of t in e=h::t matches type in specified pattern

        if type(pattern[0]) == Variable and pattern[0].get_type() == type(e[0]):
            # h in the pattern is a Variable and it type-matches h in e=h::t
            context[pattern[0].get_name()] = e[0]
            h_checks = True
        elif pattern[0] == e[0]:
            # h in the pattern matches h in e=h::t
            h_checks = True

        if type(pattern[1]) == Variable and pattern[1].get_type() == type(e[1:]):
            # t in the pattern is a Variable and it type-matches t in e=h::t
            context[pattern[1].get_name()] = e[1:]
            t_checks = True
        elif pattern[1] == e[1:]:
            # t in the pattern matches t in e=h::t
            t_checks = True

        return (h_checks and t_checks), context
    
    return False, context

def pattern_match(e, patterns):
    for pattern, command in patterns:
        types_match, context = unroll_types(e, pattern)
        if e == pattern or types_match:
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
            raise Exception(f"[Variable] type not supported; please use one of {SUPPORTED_TYPES}")
        if type(name) != str:
            raise Exception(f"[Variable] name of Variable should be type string")
        self._name = name
        self._type = t

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

### OPERATIONS ###

def search(l, el):
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([type(e) == list_type for e in l]):
        raise Exception(f"[Search] all elements of list must be of same type")
    if type(el) != list_type:
        raise Exception(f"[Search] cannot search for element in a list of a different type")

    return pattern_match(l, [
        ([], False),
        ([el], True),
        ((el, Variable("t", list)), True),
        ((Variable("h", type(el)), Variable("t", list)), "recurse t") # TODO: define cons operator instead of tuple
    ])