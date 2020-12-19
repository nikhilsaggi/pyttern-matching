Implements OCaml-style pattern matching and the Cons operator in Python.  

See below for examples of using the `pattern_match()` function:
### Example 1
#### Compute sum of a list
OCaml code:
```
let sum l =
    match l with
    | [] -> 0
    | h::t -> h + sum t
```
Python code:
```
def sum(l):
    return pattern_match(l, [
        ([], 0),
        (Cons(Variable("h", int), Variable("t", list)), Evaluation("h + FUNC(t)"))
    ])
```

### Example 2
#### Check if consecutive elements `el1` and `el2` exist in list, with one in between
OCaml code:
```
let search_two_skip l el1 el2 =
    match l with
    | [] -> false
    | el1::_::el2::t -> true
    | h::t -> search_two_skip t el1 el2
```
Python code:
```
def search_two_skip(l, el1, el2):
    return pattern_match(l, [
        ([], False),
        (Cons(el1, Wildcard(), el2, Variable("t", list)), True),
        (Cons(Variable("h", list_type), Variable("t", list)), Evaluation("FUNC(t)"))
    ])
```

### Currently implemented examples 
(see line 154 onwards in [pattern_match.py](pattern_match.py) for implementations)
* `next_highest_odd`: obtains next highest odd number
* `fib`: gets specified fibonacci number
* `search`: checks if element is in list
* `search_two`: checks if two consecutive elements are in list
* `search_two_skip`: checks if two consecutive elements are in list, with one in between
* `is_second`: checks if element is second in list
* `length`: length of list
* `sum`: sum of list of ints
* `sum_of_triple`: sum of 3-tuple of ints
* `is_double`: checks if second element of tuple is double the first element

### To do
* Deal with eval()'s incompatibility with list of strings
* Add warning system for unreachable patterns