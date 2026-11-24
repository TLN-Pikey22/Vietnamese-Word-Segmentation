
import unittest
from fmm import fmm
from bmm import bmm


class TestFMMBMM(unittest.TestCase):

    def setUp(self):
        self.dictionary = {
            "học",
            "sinh",
            "học_sinh",
            "sinh_học"
        }

        self.sentence = "học sinh học sinh học"

    def test_fmm(self):
        result = fmm(self.sentence, self.dictionary)

        expected = "học_sinh học_sinh học"

        self.assertEqual(result, expected)

    def test_bmm(self):
        result = bmm(self.sentence, self.dictionary)

        expected = "học sinh_học sinh_học"

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
