"""test lists module"""

import unittest

from nixpkgs_lib_python import fix, fix_prime, extends, fold, foldr, foldl


class TestLists(unittest.TestCase):
    """Controller for the fixed point tests"""

    def test_lists_fold(self):
        """Test lists fold"""

        fold_call = lambda f: f(lambda a: lambda b: a + b, "z")

        foldr_concat = fold_call(foldr)
        foldl_concat = fold_call(foldl)

        self.assertEqual(foldr_concat(["a", "b", "c"]), "abcz")

        self.assertEqual(foldl_concat(["a", "b", "c"]), "zabc")

        fold_second = foldl(lambda s: lambda n: s + str(n + 1))("a")
        self.assertEqual(fold_second(list(range(1, 5))), "a2345")


if __name__ == "__main__":
    unittest.main()
