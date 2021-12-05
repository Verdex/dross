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
        self.assertTrue(match.success())
        self.assertEqual(len(match.match), 4)
        self.assertEqual(match.match[0], input[0])
        self.assertEqual(match.match[1].serialize(), input[1].serialize())
        self.assertEqual(match.match[2].serialize(), input[2].serialize())
        self.assertEqual(match.match[3].serialize(), input[3].serialize())

    def test_match_array_should_not_match(self):
        input = [ parse_data("data") \
                , parse_data("data()") \
                , parse_data("data(data)") \
                , parse_data("data(data(), data)") \
                ]
        matcher = parse_matcher("data, data(), data(data), data(data(), data2)")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_array_should_match_with_star(self):
        input = [ parse_data("data") \
                , parse_data("data()") \
                , parse_data("data(data)") \
                , parse_data("data(data(), data)") \
                ]
        matcher = parse_matcher("data, *")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(len(match.match), 4)
        self.assertEqual(match.match[0], input[0])
        self.assertEqual(match.match[1].serialize(), input[1].serialize())
        self.assertEqual(match.match[2].serialize(), input[2].serialize())
        self.assertEqual(match.match[3].serialize(), input[3].serialize())

    def test_match_array_should_not_match_with_star(self):
        input = [ parse_data("data") \
                , parse_data("data()") \
                , parse_data("data(data)") \
                , parse_data("data(data(), data)") \
                ]
        matcher = parse_matcher("data2, *")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_array_should_capture(self):
        input = [ parse_data("data1") \
                , parse_data("data2()") \
                , parse_data("data3(data4)") \
                , parse_data("data5(data6(), data7)") \
                ]
        matcher = parse_matcher("D1, data2(), D3(D4), D5(D6(), D7)")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(len(match.match), 4)
        self.assertEqual(match.match[0], input[0])
        self.assertEqual(match.match[1].serialize(), input[1].serialize())
        self.assertEqual(match.match[2].serialize(), input[2].serialize())
        self.assertEqual(match.match[3].serialize(), input[3].serialize())
        self.assertTrue("D1" in match.captures)
        self.assertEqual(match.captures["D1"], "data1")
        self.assertTrue("D3" in match.captures)
        self.assertEqual(match.captures["D3"].serialize(), "data3(data4)")
        self.assertTrue("D4" in match.captures)
        self.assertEqual(match.captures["D4"], "data4")
        self.assertTrue("D5" in match.captures)
        self.assertEqual(match.captures["D5"].serialize(), "data5(data6(),data7)")
        self.assertTrue("D6" in match.captures)
        self.assertEqual(match.captures["D6"].serialize(), "data6()")
        self.assertTrue("D7" in match.captures)
        self.assertEqual(match.captures["D7"], "data7")

    def test_match_array_should_not_capture(self):
        input = [ parse_data("data1") \
                , parse_data("data2()") \
                , parse_data("data3(data4)") \
                , parse_data("data5(data6(), data7)") \
                ]
        matcher = parse_matcher("D1, dataX(), D3(D4), D5(D6(), D7)")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_array_should_capture_star(self):
        input = [ parse_data("data1") \
                , parse_data("data2()") \
                , parse_data("data3(data4)") \
                , parse_data("data5(data6(), data7)") \
                ]
        matcher = parse_matcher("D1, data2(), *")
        match = matcher.match(input)
        self.assertTrue(match.success())
        self.assertEqual(len(match.match), 4)
        self.assertEqual(match.match[0], input[0])
        self.assertEqual(match.match[1].serialize(), input[1].serialize())
        self.assertEqual(match.match[2].serialize(), input[2].serialize())
        self.assertEqual(match.match[3].serialize(), input[3].serialize())
        self.assertTrue("D1" in match.captures)
        self.assertEqual(match.captures["D1"], "data1")

    def test_match_array_should_not_capture_star(self):
        input = [ parse_data("data1") \
                , parse_data("data2()") \
                , parse_data("data3(data4)") \
                , parse_data("data5(data6(), data7)") \
                ]
        matcher = parse_matcher("D1, dataX(), *")
        match = matcher.match(input)
        self.assertFalse(match.success())

    def test_match_first_matches_first(self):
        input = [ parse_data("a()") \
                , parse_data("b(1)") \
                , parse_data("c(2)") \
                , parse_data("b(3)") \
                , parse_data("c(4)") \
                , parse_data("b(5)") \
                , parse_data("c(6)") \
                ]
        matcher = parse_matcher("b(X), c(4)")
        match = matcher.match_first(input)
        self.assertTrue(match.success())
        self.assertEqual(len(match.match), 2)
        self.assertEqual(match.match[0].serialize(), "b(3)")
        self.assertEqual(match.match[1].serialize(), "c(4)")
        self.assertTrue("X" in match.captures)
        self.assertEqual(match.captures["X"], "3")
            
    def test_match_all_matches_all(self):
        input = [ parse_data("a()") \
                , parse_data("b(1)") \
                , parse_data("c(2)") \
                , parse_data("b(3)") \
                , parse_data("c(4)") \
                , parse_data("b(5)") \
                , parse_data("c(6)") \
                , parse_data("b(5)") \
                , parse_data("c(4)") \
                ]
        matcher = parse_matcher("b(X), c(4)")
        match = matcher.match_all(input)
        self.assertEqual(len(match), 2)
        self.assertTrue(match[0].success())
        self.assertEqual(len(match[0].match), 2)
        self.assertEqual(match[0].match[0].serialize(), "b(3)")
        self.assertEqual(match[0].match[1].serialize(), "c(4)")
        self.assertTrue("X" in match[0].captures)
        self.assertEqual(match[0].captures["X"], "3")

        self.assertTrue(match[1].success())
        self.assertEqual(len(match[1].match), 2)
        self.assertEqual(match[1].match[0].serialize(), "b(5)")
        self.assertEqual(match[1].match[1].serialize(), "c(4)")
        self.assertTrue("X" in match[1].captures)
        self.assertEqual(match[1].captures["X"], "5")

if __name__ == '__main__':
    unittest.main()