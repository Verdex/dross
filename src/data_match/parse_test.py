import unittest

from .matching import *
from .parse import *

class ParseTest(unittest.TestCase):

    def test_parse_matcher_should_generate_match_any_string(self):
        output = parse_matcher(".")
        self.assertTrue(type(output) is MatchAnyString)
        
    def test_parse_matcher_should_generate_match_until_end(self):
        output = parse_matcher("*")
        self.assertTrue(type(output) is MatchUntilEnd)

    def test_parse_matcher_should_generate_capture_string(self):
        output = parse_matcher("String")
        self.assertTrue(type(output) is CaptureString)
        self.assertEqual(output.capture_name, "String")

    def test_parse_matcher_should_generate_match_string_with_value(self):
        output = parse_matcher("string")
        self.assertTrue(type(output) is MatchStringWithValue)
        self.assertEqual(output.value, "string")


if __name__ == '__main__':
    unittest.main()