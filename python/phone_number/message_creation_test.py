import unittest
from message_creation import get_potential_messages


class TestMessageCreation(unittest.TestCase):
    def testBasicCase(self):
        _input = "23"
        expected = ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]
        self.assertEqual(get_potential_messages(_input), expected)

    def testSingleString(self):
        _input = "2"
        expected = ["a", "b", "c"]
        self.assertEqual(get_potential_messages(_input), expected)

    def testEmptyCase(self):
        _input = ""
        expected = []
        self.assertEqual(get_potential_messages(_input), expected)
