import unittest

from .matching import *
from .parse import *

class MatchingTest(unittest.TestCase):

    # a = a => M: a
    # a = A => M: a, A = a
    # a = . => M: a
    # a = b => M:
    # a = * => M: a
    # a, b = * => M: [a, b]
    # a, b = a, b => M: [a, b]
    # a, b = A, B => M: [a, b], A = a, B = b
    # a = a() => M:

    # a() = a => M:
    # a() = a() => M: a()
    # a() = A() => M: a(), A = a()
    # a() = . => M:
    # a() = * => M: a()
    # a(P+) = * => M: a(P+)
    # a(P+) = . => M: 
    # a(P+) = A(P+) => M: a(P+), A = a(P+), ...
    # a(P+) = a(P+) => M: a(P+),  ...
    # a(1, 2, 3) = a(1, *) => M: a(1, 2, 3)
    # a(), b() = a(), b() => M: [a(), b()]
    # a(), b() = * => M: [a(), b()]
    # a(), b() = A(), B() => M: [a(), b()], A = a(), B = b()

    def test_match_data_should_not_match_string(self):
        input = parse_data("blah()")
        matcher = parse_matcher("blah")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_string_should_not_match_data(self):
        input = parse_data("blah")
        matcher = parse_matcher("blah()")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_string_should_not_be_data_captured(self):
        input = parse_data("blah")
        matcher = parse_matcher("A()")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_should_match_star(self):
        input = parse_data("blah(1,2,3)")
        matcher = parse_matcher("*")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(match.match.serialize(), input.serialize())

    def test_match_should_match_internal_star(self):
        input = parse_data("blah(1,2,3)")
        matcher = parse_matcher("blah(1, *)")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(match.match.serialize(), input.serialize())

    def test_match_should_capture_internal_star(self):
        input = parse_data("blah(1,2,3)")
        matcher = parse_matcher("A(1, *)")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(match.match.serialize(), input.serialize())
        self.assertTrue("A" in match.captures)
        self.assertEqual(match.captures["A"].serialize(), input.serialize())

    def test_match_string_should_match_dot(self):
        input = parse_data("blah")
        matcher = parse_matcher(".")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertTrue(type(match.match) is str)
        self.assertEqual(match.match, input)

    def test_match_string_should_match_star(self):
        input = parse_data("blah")
        matcher = parse_matcher("*")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertTrue(type(match.match) is str)
        self.assertEqual(match.match, input)

    def test_match_string_should_not_match(self):
        input = parse_data("blah")
        matcher = parse_matcher("other")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_data_should_not_match_dot(self):
        input = parse_data("blah()")
        matcher = parse_matcher(".")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_should_capture_string(self): 
        input = parse_data("blah")
        matcher = parse_matcher("X")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertTrue("X" in match.captures)
        self.assertEqual(match.captures["X"], "blah")

    def test_match_should_capture_data(self):
        input = parse_data("data()")
        matcher = parse_matcher("X()")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertTrue("X" in match.captures)
        self.assertEqual(match.captures["X"].serialize(), input.serialize())

    def test_match_data_should_match_data(self):
        input = parse_data("data()")
        matcher = parse_matcher("data()")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(match.match.serialize(), input.serialize())

    def test_match_data_should_not_match_data(self):
        input = parse_data("data()")
        matcher = parse_matcher("other()")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_data_should_match_recursive_data(self):
        input = parse_data("data(1, 2, inner(1, 2), 3)")
        matcher = parse_matcher("data(1, 2, inner(1, 2), 3)")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(match.match.serialize(), input.serialize())

    def test_match_data_should_not_match_recursive_data(self):
        input = parse_data("data(1, 2, inner(x, 2), 3)")
        matcher = parse_matcher("data(1, 2, inner(1, 2), 3)")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_data_should_capture_recursive_data(self):
        input = parse_data("data(1, 2, inner(1, 2), 3)")
        matcher = parse_matcher("Data(A, 2, Inner(1, 2), 3)")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(match.match.serialize(), input.serialize())
        self.assertTrue("Data" in match.captures)
        self.assertEqual(match.captures["Data"].serialize(), input.serialize())
        self.assertTrue("Inner" in match.captures)
        self.assertEqual(match.captures["Inner"].serialize(), "inner(1,2)")
        self.assertTrue("A" in match.captures)
        self.assertEqual(match.captures["A"], "1")

    def test_match_data_should_not_capture_recursive_data(self):
        input = parse_data("data(1, 2, inner(1, 2), 3)")
        matcher = parse_matcher("Data(A, 2, Inner(1, 2), x)")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_array_should_match(self):
        input = [ parse_data("data") \
                , parse_data("data()") \
                , parse_data("data(data)") \
                , parse_data("data(data(), data)") \
                ]
        matcher = parse_matcher("data, data(), data(data), data(data(), data)")
        match = matcher.match(input)
        self.assertTrue(match.success)
        self.assertEqual(len(match.match), 4)
        self.assertEqual(match.match[0], input[0])
        self.assertEqual(match.match[1].serialize(), input[1].serialize())
        self.assertEqual(match.match[2].serialize(), input[2].serialize())
        self.assertEqual(match.match[3].serialize(), input[3].serialize())

    # * 
    # capture
    # capture *
    # not match 
    # not match *
    # not capture
    # not capture *

            
if __name__ == '__main__':
    unittest.main()