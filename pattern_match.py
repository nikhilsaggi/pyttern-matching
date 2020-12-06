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

    if isinstance(pattern, tuple): # TODO: define cons operator instead of tuple
        # Cons
        if len(pattern) > len(e)+1:
            # pattern we are trying to apply is larger than Cons; quit
            return False, context

        checks = [False]*len(pattern)

        for i in range(len(pattern) - 1):
            if isinstance(pattern[i], Variable) and pattern[i].get_type() == type(e[i]):
                # element i in the pattern is a Variable and it type-matches i in e=(... :: i :: ... :: t)
                context[pattern[i].get_name()] = e[i]
                checks[i] = True
            elif pattern[i] == e[i] or isinstance(pattern[i], Wildcard):
                # element i in the pattern equals i in e=(... :: i  :: ... :: t) or is wildcard
                checks[i] = True

        last = len(pattern) - 1
        if isinstance(pattern[last], Variable) and pattern[last].get_type() == type(e[last:]):
            # t in the pattern is a Variable and it type-matches t in e=h::t
            context[pattern[last].get_name()] = e[last:]
            checks[last] = True
        elif pattern[last] == e[last:]:
            # t in the pattern matches t in e=h::t
            checks[last] = True

        return all(checks), context
    
    return False, context

def pattern_match(e, patterns):
    for pattern, command in patterns:
        if isinstance(pattern, Wildcard):
            return command

        types_match, context = unroll_types(e, pattern)
        if e == pattern or types_match:
            if isinstance(command, str) and command.startswith('recurse'):
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
        if not isinstance(name, str):
            raise Exception(f"[Variable] name of Variable should be type string")
        self._name = name
        self._type = t

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type

class Wildcard:
    def __init__(self):
        pass

### OPERATIONS ###

def search(l, el):
    """
    Returns True if el is in l.

    Args:
        l
            A list where each element is of type t
        el
            An element of type t
    """
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[search] all elements of l must be of same type")
    if not isinstance(el, list_type):
        raise Exception(f"[search] el not same type as list elements")

    return pattern_match(l, [
        ([], False),
        ((el, Variable("t", list)), True),
        ((Variable("h", list_type), Variable("t", list)), "recurse t") # TODO: define cons operator instead of tuple
    ])

def search_two(l, el1, el2):
    """
    Returns True if el1 and el2 are found in succession in l.

    Args:
        l
            A list where each element is of type t
        el1
            An element of type t
        el2
            An element of type t
    """ 
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[search_two] all elements of l must be of same type")
    if not isinstance(el1, list_type):
        raise Exception(f"[search_two] el1 not same type as list elements")
    if not isinstance(el2, list_type):
        raise Exception(f"[search_two] el2 not same type as list elements")

    return pattern_match(l, [
        ([], False),
        ((el1, el2, Variable("t", list)), True),
        ((Variable("h", list_type), Variable("t", list)), "recurse t") # TODO: define cons operator instead of tuple
    ])

def search_two_skip(l, el1, el2):
    """
    Returns True if el1 and el2 are found in succession, with one element between them, in l.

    Args:
        l
            A list where each element is of type t
        el1
            An element of type t
        el2
            An element of type t
    """ 
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[search_two_skip] all elements of l must be of same type")
    if not isinstance(el1, list_type):
        raise Exception(f"[search_two_skip] el1 not same type as list elements")
    if not isinstance(el2, list_type):
        raise Exception(f"[search_two_skip] el2 not same type as list elements")

    return pattern_match(l, [
        ([], False),
        ((el1, Wildcard(), el2, Variable("t", list)), True),
        ((Variable("h", list_type), Variable("t", list)), "recurse t") # TODO: define cons operator instead of tuple
    ])


def is_second(l, el):
    """
    Returns True if el is the second element of l.

    Args:
        l
            A list where each element is of type t
        el
            An element of type t
    """
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[is_second] all elements of l must be of same type")
    if not isinstance(el, list_type):
        raise Exception(f"[is_second] el not same type as list elements")

    return pattern_match(l, [
        ((Variable("e1", list_type), el, Variable("t", list)), True),
        (Wildcard(), False)
    ])