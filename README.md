Implements OCaml-style pattern matching and the Cons operator in Python.  
See OPERATIONS section in `pattern_match.py` for examples on how to write pattern matches.  


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
* `search`: checks if element is in list
* `search_two`: checks if two consecutive elements are in list
* `is_second`: checks if element is second in list

### To do
* Implement Cons operator
* Support non-list pattern matching
* Add warning system for missing or unreachable patterns