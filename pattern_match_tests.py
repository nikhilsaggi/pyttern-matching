import pattern_match

assert pattern_match.search([], 1) == False

assert pattern_match.search([2], 1) == False
assert pattern_match.search([3], 3) == True

assert pattern_match.search([8, 5], 8) == True
assert pattern_match.search([8, 5], 5) == True
assert pattern_match.search([8, 5], 0) == False

assert pattern_match.search([8, 10, 5], 8) == True
assert pattern_match.search([8, 10, 5], 10) == True
assert pattern_match.search([8, 10, 5], 5) == True
assert pattern_match.search([8, 10, 5], 7) == False

assert pattern_match.search(["a", "b"], "a") == True
assert pattern_match.search(["a", "b"], "b") == True
assert pattern_match.search(["a", "b"], "c") == False

assert pattern_match.search([True, False], True) == True
assert pattern_match.search([True, False], False) == True
assert pattern_match.search([True, True], False) == False