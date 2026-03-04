import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        firstLine = "# This is the title"
        self.assertEqual(extract_title(firstLine), "This is the title")
        firstLineWithoutSpace = "#This is also a title"
        self.assertEqual(extract_title(firstLineWithoutSpace), "This is also a title")
        multiLine = "This is the first line and has nothing to do with anything\n# Here comes the title"
        self.assertEqual(extract_title(multiLine), "Here comes the title")

if __name__ == "__main__":
    unittest.main()