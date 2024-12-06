"""test lists module"""

import unittest

from nixpkgs_lib_python import fix, fix_prime, extends, fold, foldr


class TestLists(unittest.TestCase):
    """Controller for the fixed point tests"""

    def test_lists_fold(self):
        """Test lists fold"""

        fold_call = lambda f: f(lambda a, b: a + b, "z", ["a", "b", "c"])

        self.assertEqual(fold_call(foldr), "abcz")
        self.assertEqual(fold_call(fold), "abcz")


if __name__ == "__main__":
    unittest.main()
