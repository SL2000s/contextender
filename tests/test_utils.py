import unittest

from contextender.utils import text_splitter


class TestTextSplitter(unittest.TestCase):

    def test_no_separator(self):
        text = "This is a sample text for testing."
        max_chars = 10
        expected = ["This is a ", "sample tex", "t for test", "ing."]
        result = list(text_splitter(text, max_chars))
        self.assertEqual(result, expected)

    def test_with_separator(self):
        text = "This is a sample text for testing."
        max_chars = 10
        separator = " "
        expected = ["This is a", " sample", " text for", " testing."]
        result = list(text_splitter(text, max_chars, separator))
        self.assertEqual(result, expected)

    def test_long_word(self):
        text = "Thisisaverylongwordthatneedstobesplit."
        max_chars = 10
        expected = ["Thisisaver", "ylongwordt", "hatneedsto", "besplit."]
        result = list(text_splitter(text, max_chars))
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text = ""
        max_chars = 10
        expected = []
        result = list(text_splitter(text, max_chars))
        self.assertEqual(result, expected)

    def test_separator_longer_than_max_chars(self):
        text = "This is a sample text for testing."
        max_chars = 5
        separator = "sample"
        expected = [
            "This",
            " is a",
            " samp",
            "le",
            " text",
            " for",
            " test",
            "ing.",
        ]
        result = list(text_splitter(text, max_chars, separator))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
