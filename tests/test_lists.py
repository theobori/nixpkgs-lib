"""test lists module"""

import unittest

from nixpkgs_lib_python import fix, fix_prime, extends, fold, foldr


class TestLists(unittest.TestCase):
    """Controller for the fixed point tests"""

    def test_lists_fold(self):
        """Test lists fold"""

        fold_call = lambda f: f(lambda a: lambda b: a + b, "z", ["a", "b", "c"])

        concat = foldr(lambda a: lambda b: a + b, "z")

        self.assertEqual(concat(["a", "b", "c"]), "abcz")


if __name__ == "__main__":
    unittest.main()
