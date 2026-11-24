
import unittest
from hmm import viterbi


class TestViterbi(unittest.TestCase):

    def test_viterbi_three_syllables(self):
        model = {
            "states": ["B", "I"],
            "vocabulary": {"x", "y", "z"},
            "start_prob": {
                "B": 0.8,
                "I": 0.2
            },
            "transition_prob": {
                "B": {"B": 0.4, "I": 0.6},
                "I": {"B": 0.7, "I": 0.3}
            },
            "emission_prob": {
                "B": {"x": 0.5, "y": 0.2, "z": 0.3},
                "I": {"x": 0.1, "y": 0.6, "z": 0.3}
            }
        }

        result = viterbi("x y z", model)

        expected = "x_y z"

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
