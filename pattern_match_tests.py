import pattern_match

assert pattern_match.search([], 1) == False
assert pattern_match.search([2], 1) == False
assert pattern_match.search([3], 3) == True
assert pattern_match.search([8, 5], 5) == True
assert pattern_match.search([8, 10, 5], 5) == True