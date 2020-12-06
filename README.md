Implements OCaml-style pattern matching and the Cons operator in Python.  
See OPERATIONS section in [pattern_match.py](pattern_match.py) for examples on how to write pattern matches.  


See below for an example on how to use implemented functions:

```
>>> import pattern_match
>>> pattern_match.search([8,10,5], 5)
True
>>> pattern_match.search_two([8,10,5], 10, 5)
True
>>> pattern_match.search([8,10,5], 1)
False
```

### Currently implemented examples
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