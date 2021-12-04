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

    def test_parse_matcher_should_generate_match_data_with_name(self):
        output = parse_matcher("string()")
        self.assertTrue(type(output) is MatchDataWithName)
        self.assertEqual(output.target_name, "string")

    def test_parse_matcher_should_generate_capture_data(self):
        output = parse_matcher("String()")
        self.assertTrue(type(output) is CaptureData)
        self.assertEqual(output.capture_name, "String")

    def test_parse_matcher_should_generate_capture_data_with_sub_matchers(self):
        output = parse_matcher("String(a, ., X(), a(), *)")
        self.assertTrue(type(output) is CaptureData)
        self.assertEqual(output.capture_name, "String")
        self.assertEqual(len(output.sub_matchers), 5)
        self.assertTrue(type(output.sub_matchers[0]) is MatchStringWithValue)
        self.assertTrue(type(output.sub_matchers[1]) is MatchAnyString)
        self.assertTrue(type(output.sub_matchers[2]) is CaptureData)
        self.assertTrue(type(output.sub_matchers[3]) is MatchDataWithName)
        self.assertTrue(type(output.sub_matchers[4]) is MatchUntilEnd)

    def test_parse_matcher_should_generate_match_data_with_name_with_sub_matchers(self):
        output = parse_matcher("string(a, ., X(), a(), *)")
        self.assertTrue(type(output) is MatchDataWithName)
        self.assertEqual(output.target_name, "string")
        self.assertEqual(len(output.sub_matchers), 5)
        self.assertTrue(type(output.sub_matchers[0]) is MatchStringWithValue)
        self.assertTrue(type(output.sub_matchers[1]) is MatchAnyString)
        self.assertTrue(type(output.sub_matchers[2]) is CaptureData)
        self.assertTrue(type(output.sub_matchers[3]) is MatchDataWithName)
        self.assertTrue(type(output.sub_matchers[4]) is MatchUntilEnd)

if __name__ == '__main__':
    unittest.main()