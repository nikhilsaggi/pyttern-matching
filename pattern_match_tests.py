import pattern_match

def next_highest_odd_tests():
    assert pattern_match.next_highest_odd(0) == 1
    assert pattern_match.next_highest_odd(1) == 3
    assert pattern_match.next_highest_odd(2) == 3
    assert pattern_match.next_highest_odd(3) == 5
    assert pattern_match.next_highest_odd(4) == 5
    assert pattern_match.next_highest_odd(5) == 7
    assert pattern_match.next_highest_odd(6) == 7
    assert pattern_match.next_highest_odd(7) == 9
    assert pattern_match.next_highest_odd(8) == 9
    assert pattern_match.next_highest_odd(9) == 11


def fib_tests():
    assert pattern_match.fib(1) == 1
    assert pattern_match.fib(2) == 1
    assert pattern_match.fib(3) == 2
    assert pattern_match.fib(4) == 3
    assert pattern_match.fib(5) == 5
    assert pattern_match.fib(6) == 8
    assert pattern_match.fib(7) == 13
    assert pattern_match.fib(8) == 21
    assert pattern_match.fib(9) == 34
    assert pattern_match.fib(10) == 55
    

def search_tests():
    assert pattern_match.search([], 1) == False

    assert pattern_match.search([3], 3) == True
    assert pattern_match.search([2], 1) == False

    assert pattern_match.search([8, 5], 8) == True
    assert pattern_match.search([8, 5], 5) == True
    assert pattern_match.search([8, 5], 0) == False

    assert pattern_match.search([8, 10, 5], 8) == True
    assert pattern_match.search([8, 10, 5], 10) == True
    assert pattern_match.search([8, 10, 5], 5) == True
    assert pattern_match.search([8, 10, 5], 7) == False

    # assert pattern_match.search(["a", "b"], "a") == True
    # assert pattern_match.search(["a", "b"], "b") == True
    # assert pattern_match.search(["a", "b"], "c") == False

    assert pattern_match.search([True, False], True) == True
    assert pattern_match.search([True, False], False) == True
    assert pattern_match.search([True, True], False) == False


def search_two_tests():
    assert pattern_match.search_two([], 1, 1) == False
    assert pattern_match.search_two([3], 3, 1) == False

    assert pattern_match.search_two([8, 5], 8, 5) == True
    assert pattern_match.search_two([8, 5], 8, 6) == False
    assert pattern_match.search_two([8, 5], 5, 8) == False
    assert pattern_match.search_two([8, 5], 0, 0) == False

    assert pattern_match.search_two([8, 10, 5], 8, 10) == True
    assert pattern_match.search_two([8, 10, 5], 10, 5) == True
    assert pattern_match.search_two([8, 10, 5], 8, 5) == False
    assert pattern_match.search_two([8, 10, 5], 8, 8) == False

    # assert pattern_match.search_two(["a", "b"], "a", "b") == True
    # assert pattern_match.search_two(["a", "b"], "b", "b") == False
    # assert pattern_match.search_two(["a", "b"], "c", "d") == False

    assert pattern_match.search_two([True, False], True, False) == True
    assert pattern_match.search_two([True, False], False, True) == False
    assert pattern_match.search_two([True, True], True, False) == False


def search_two_skip_tests():
    assert pattern_match.search_two_skip([], 1, 1) == False
    assert pattern_match.search_two_skip([3], 3, 1) == False
    assert pattern_match.search_two_skip([8, 5], 8, 5) == False

    assert pattern_match.search_two_skip([8, 10, 5], 8, 5) == True
    assert pattern_match.search_two_skip([8, 10, 5], 8, 10) == False
    assert pattern_match.search_two_skip([8, 10, 5], 8, 8) == False
    assert pattern_match.search_two_skip([8, 10, 5], 10, 5) == False
    assert pattern_match.search_two_skip([8, 10, 5], 5, 8) == False

    assert pattern_match.search_two_skip([1, 3, 5, 7], 1, 5) == True
    assert pattern_match.search_two_skip([1, 3, 5, 7], 3, 7) == True
    assert pattern_match.search_two_skip([1, 3, 5, 7], 1, 7) == False

    # assert pattern_match.search_two_skip(["a", "b"], "a", "b") == False
    # assert pattern_match.search_two_skip(["a", "b", "c"], "a", "c") == True
    # assert pattern_match.search_two_skip(["a", "b", "c"], "c", "d") == False

    assert pattern_match.search_two_skip([True, False], True, False) == False
    assert pattern_match.search_two_skip([True, False, True], True, True) == True
    assert pattern_match.search_two_skip([True, False, True], False, False) == False
    assert pattern_match.search_two_skip([True, True, True], True, True) == True


def is_second_tests():
    assert pattern_match.is_second([], 1) == False
    assert pattern_match.is_second([2], 1) == False

    assert pattern_match.is_second([8, 5], 8) == False
    assert pattern_match.is_second([8, 5], 5) == True
    assert pattern_match.is_second([8, 5], 0) == False
    assert pattern_match.is_second([5, 5], 5) == True

    assert pattern_match.is_second([8, 10, 5], 8) == False
    assert pattern_match.is_second([8, 10, 5], 10) == True
    assert pattern_match.is_second([8, 10, 5], 5) == False
    assert pattern_match.is_second([8, 10, 5], 7) == False
    assert pattern_match.is_second([10, 10, 5], 10) == True
    assert pattern_match.is_second([8, 10, 10], 10) == True

    # assert pattern_match.is_second(["a", "b"], "a") == False
    # assert pattern_match.is_second(["a", "b"], "b") == True
    # assert pattern_match.is_second(["a", "b"], "c") == False

    assert pattern_match.is_second([True, False], True) == False
    assert pattern_match.is_second([True, False], False) == True
    assert pattern_match.is_second([True, True], False) == False


def length_tests():
    assert pattern_match.length([]) == 0
    assert pattern_match.length([1]) == 1
    assert pattern_match.length([18]) == 1
    assert pattern_match.length([10, 20, 35]) == 3
    assert pattern_match.length([10, 20, 35, 54, -2345, 210]) == 6
    assert pattern_match.length([False, True, True, True]) == 4


def sum_tests():
    assert pattern_match.sum([]) == 0
    assert pattern_match.sum([1]) == 1
    assert pattern_match.sum([18]) == 18
    assert pattern_match.sum([10, 20, 35]) == 65
    assert pattern_match.sum([10, 20, 35, 54, -2345, 210]) == -2016


def sum_of_triple_tests():
    assert pattern_match.sum_of_triple((1,)) == None
    assert pattern_match.sum_of_triple((2, 4)) == None
    assert pattern_match.sum_of_triple((10, 2, 10, 50)) == None

    assert pattern_match.sum_of_triple((1, 5, 10)) == 16
    assert pattern_match.sum_of_triple((-5, 20, 4)) == 19
    assert pattern_match.sum_of_triple((100, 1000, 10000)) == 11100
    assert pattern_match.sum_of_triple((0, 0, 0)) == 0


def is_double_tests():
    assert pattern_match.is_double((1,)) == False
    assert pattern_match.is_double((2, 4, 8)) == False
    assert pattern_match.is_double((10, 2, 10, 50)) == False

    assert pattern_match.is_double((15, 30)) == True
    assert pattern_match.is_double((2, 4)) == True
    assert pattern_match.is_double((0, 0)) == True
    assert pattern_match.is_double((4, 2)) == False
    assert pattern_match.is_double((-10, -20)) == True
    assert pattern_match.is_double((-10, 20)) == False
    assert pattern_match.is_double((0, 5)) == False
    assert pattern_match.is_double((5, 0)) == False
    assert pattern_match.is_double((1, 1)) == False


if __name__ == '__main__':
    # no data structures
    next_highest_odd_tests()
    fib_tests()

    # cons
    search_tests()
    search_two_tests()
    search_two_skip_tests()
    is_second_tests()
    length_tests()
    sum_tests()

    # tuple
    sum_of_triple_tests()
    is_double_tests()