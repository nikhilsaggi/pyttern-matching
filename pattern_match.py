import re

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

    if isinstance(pattern, Cons):
        if len(pattern) > len(e)+1:
            # pattern we are trying to apply is larger than Cons; quit
            # (+1 because last element of valid Cons can be [])
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

    elif isinstance(pattern, tuple):
        if len(pattern) != len(e):
            return False, context

        checks = [False]*len(pattern)

        for i in range(len(pattern)):
            if isinstance(pattern[i], Variable) and pattern[i].get_type() == type(e[i]):
                # element i in the pattern is a Variable and it type-matches i in e=(..., i, ...)
                context[pattern[i].get_name()] = e[i]
                checks[i] = True
            elif pattern[i] == e[i] or isinstance(pattern[i], Wildcard):
                # element i in the pattern equals i in e=(..., i, ...) or is wildcard
                checks[i] = True

        return all(checks), context

    elif isinstance(pattern, Variable):
        context[pattern.get_name()] = e
        return True, context
    
    return False, context

def pattern_match(e, patterns):
    for pattern, command in patterns:
        if isinstance(pattern, Wildcard):
            return command

        types_match, context = unroll_types(e, pattern)
        if e == pattern or types_match:
            if isinstance(command, Evaluation):
                com = command.get()
                # replace all FUNC(...) with pattern_match(..., patterns)
                funcs = [m.start() for m in re.finditer('FUNC\(', com)]
                if funcs != []:
                    # recursive call used
                    try:
                        for func_id in funcs[::-1]:
                            # flip funcs so that we access indices right-to-left, so they don't get shifted right
                            id = com.find(")", func_id)
                            com = com[:id] + ", patterns" + com[id:]
                    except ValueError:
                        raise Exception("[pattern_match] invalid Recursive call syntax")
                    com = com.replace("FUNC", "pattern_match")

                # declare all variables defined in pattern
                for var, val in context.items():
                    exec(var + "=" + str(val)) # TODO: this breaks lists of string elements

                # execute recursive call
                exec("return_val=" + com)
                return locals()['return_val']
            else:
                return command
                
    raise Exception("[pattern_match] pattern matching is not exhaustive")

### DATA STRUCTURES ###

class Cons:
    def __init__(self, *args):
        # nested definition (annoying, don't use)
        # if len(args) > 1:
        #     self._data = (args[0], Cons(*args[1:]))
        # else:
        #     self._data = (args[0], [])

        self._data = args

    def hd(self):
        return self._data[0]

    def tl(self):
        return self._data[1:]

    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, key):
        return self._data[key]


class Variable:
    def __init__(self, name, t):
        if t not in SUPPORTED_TYPES:
            raise Exception(f"[Variable] type {t} not supported; please use one of {SUPPORTED_TYPES}")
        if not isinstance(name, str):
            raise Exception(f"[Variable] {name} should be type str")
        self._name = name
        self._type = t

    def get_name(self):
        return self._name

    def get_type(self):
        return self._type


class Wildcard:
    def __init__(self):
        pass


class Evaluation:
    def __init__(self, s):
        if not isinstance(s, str):
            raise Exception(f"[Evaluation] {s} should be type str")
        self._data = s

    def get(self):
        return self._data

### OPERATIONS ###

# No data structure #

def next_highest_odd(n):
    """
    Returns next highest odd number after n.

    Args:
        n:
            An int

    OCaml equivalent:
        match n with
        | i -> if i mod 2 = 0 then i+1 else i+2
    """
    if not isinstance(n, int):
        raise Exception(f"[next_highest_odd] {n} must be int")

    return pattern_match(n, [
        (Variable("i", int), Evaluation("i+1 if i%2 == 0 else i+2"))
    ])


def fib(n):
    """
    Returns the n-th fibonacci number.

    Args:
        n:
            An int greater than 0

    OCaml equivalent:
        match n with
        | 1 -> 1
        | 2 -> 1
        | i -> (fib i-1) + (fib i-2)
    """
    if not isinstance(n, int):
        raise Exception(f"[fib] {n} must be int")

    if n < 1:
        raise Exception(f"[fib] {n} must be >=1")

    return pattern_match(n, [
        (1, 1),
        (2, 1),
        (Variable("i", int), Evaluation("FUNC(i-1) + FUNC(i-2)"))
    ])

# Cons #

def search(l, el):
    """
    Returns True if el is in l.

    Args:
        l:
            A list where each element is of type t
        el:
            An element of type t

    OCaml equivalent:
        match l with
        | [] -> false
        | el::t -> true
        | h::t -> search t el
    """
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[search] all elements of {l} must be of same type")
    if not isinstance(el, list_type):
        raise Exception(f"[search] {el} not same type as list elements")

    return pattern_match(l, [
        ([], False),
        (Cons(el, Variable("t", list)), True),
        (Cons(Variable("h", list_type), Variable("t", list)), Evaluation("FUNC(t)"))
    ])


def search_two(l, el1, el2):
    """
    Returns True if el1 and el2 are found in succession in l.

    Args:
        l:
            A list where each element is of type t
        el1:
            An element of type t
        el2:
            An element of type t

    OCaml equivalent:
        match l with
        | [] -> false
        | el1::el2::t -> true
        | h::t -> search_two t el1 el2
    """ 
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[search_two] all elements of {l} must be of same type")
    if not isinstance(el1, list_type):
        raise Exception(f"[search_two] {el1} not same type as list elements")
    if not isinstance(el2, list_type):
        raise Exception(f"[search_two] {el2} not same type as list elements")

    return pattern_match(l, [
        ([], False),
        (Cons(el1, el2, Variable("t", list)), True),
        (Cons(Variable("h", list_type), Variable("t", list)), Evaluation("FUNC(t)"))
    ])


def search_two_skip(l, el1, el2):
    """
    Returns True if el1 and el2 are found in succession, with one element between them, in l.

    Args:
        l:
            A list where each element is of type t
        el1:
            An element of type t
        el2:
            An element of type t

    OCaml equivalent:
        match l with
        | [] -> false
        | el1::_::el2::t -> true
        | h::t -> search_two_skip t el1 el2
    """ 
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[search_two_skip] all elements of {l} must be of same type")
    if not isinstance(el1, list_type):
        raise Exception(f"[search_two_skip] {el1} not same type as list elements")
    if not isinstance(el2, list_type):
        raise Exception(f"[search_two_skip] {el2} not same type as list elements")

    return pattern_match(l, [
        ([], False),
        (Cons(el1, Wildcard(), el2, Variable("t", list)), True),
        (Cons(Variable("h", list_type), Variable("t", list)), Evaluation("FUNC(t)"))
    ])


def is_second(l, el):
    """
    Returns True if el is the second element of l.

    Args:
        l:
            A list where each element is of type t
        el:
            An element of type t

    OCaml equivalent:
        match l with
        | _::el::t -> true
        | _ -> false
    """
    if l == []:
        return False
    
    list_type = type(l[0])
    if not all([isinstance(e, list_type) for e in l]):
        raise Exception(f"[is_second] all elements of {l} must be of same type")
    if not isinstance(el, list_type):
        raise Exception(f"[is_second] {el} not same type as list elements")

    return pattern_match(l, [
        (Cons(Variable("e1", list_type), el, Variable("t", list)), True),
        (Wildcard(), False)
    ])


def length(l):
    """
    Returns length of l.

    Args:
        l:
            A list of ints

    OCaml equivalent:
        match l with
        | [] -> 0
        | h::t -> 1 + sum t
    """
    list_type = int # doesn't really matter, we will overwrite it below if we need it
    if l != []:
        list_type = type(l[0])

    return pattern_match(l, [
        ([], 0),
        (Cons(Variable("h", list_type), Variable("t", list)), Evaluation("1 + FUNC(t)"))
    ])


def sum(l):
    """
    Returns sum of elements of l.

    Args:
        l:
            A list of ints

    OCaml equivalent:
        match l with
        | [] -> 0
        | h::t -> h + sum t
    """
    if l == []:
        return False
    
    if not all([isinstance(e, int) for e in l]):
        raise Exception(f"[sum] all elements of {l} must be of type int")

    return pattern_match(l, [
        ([], 0),
        (Cons(Variable("h", int), Variable("t", list)), Evaluation("h + FUNC(t)"))
    ])

# Tuple #

def sum_of_triple(t):
    """
    Returns sum of 3-tuple of ints. Returns None if tuple is not size 3.

    Args:
        t:
            A tuple of ints
    
    OCaml equivalent:
        match t with
        | (x,y,z) -> Some (x+y+z)
        | _ -> None
    """
    if not all([isinstance(i, int) for i in t]):
        raise Exception(f"[sum_of_triple] {t} should contain ints")

    return pattern_match(t, [
        ((Variable("x", int), Variable("y", int), Variable("z", int)), Evaluation("x+y+z")),
        (Wildcard(), None)
    ])


def is_double(t):
    """
    Returns True if 2nd element in the tuple is 2x the 1st element. Returns False if tuple is not size 2.

    Args:
        t:
            A tuple of ints

    OCaml equivalent:
        match t with
        | (x,y) -> if y=2*x then true else false
        | _ -> false
    """
    if not all([isinstance(i, int) for i in t]):
        raise Exception(f"[is_double] {t} should contain ints")

    return pattern_match(t, [
        ((Variable("x", int), Variable("y", int)), Evaluation("True if y==2*x else False")),
        (Wildcard(), False)
    ])