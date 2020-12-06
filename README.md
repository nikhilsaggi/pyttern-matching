Implements OCaml-style pattern matching and the Cons operator in Python. See below for an example on how to use:

```
>>> import pattern_match
>>> pattern_match.search([10,10,5], 10)
True
>>> pattern_match.search([10,10,5], 5)
True
>>> pattern_match.search([10,10,5], 9999)
False
```

### To do
* Implement Cons operator
* Implement wildcards
* Support non-list pattern matching
* Add warning system for missing or unreachable patterns