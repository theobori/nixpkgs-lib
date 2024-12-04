"""test laziness module"""

import unittest

from nixpkgs_lib_python import fix, fix_prime


class TestFixedPoint(unittest.TestCase):
    """Controller for the fixed point tests"""

    def test_fixed_point_dict(self):
        """Test fixed point with a dict"""

        attrs_function = lambda self: {
            "n": [1, "1", 3, 4],
            "a": 3,
            "b": int(self["n"][1] + "2") + self["n"][0],
            "c": self["a"] - 12,
            "d": self["a"],
            "e": self["a"] > 1,
        }

        attrs = fix(attrs_function)

        self.assertEqual(attrs["c"], -9)

        attrs = fix_prime(attrs_function)

        self.assertTrue("__unfix__" in attrs)

    def test_fixed_point_list(self):
        """Test fixed point with a list"""

        it_function = lambda self: [
            "hello",
            self[0] + " world " + self[0],
            self[1] + "world",
            self[0] == "hello",
        ]

        it = fix(it_function)

        self.assertEqual(it[1], "hello world hello")


if __name__ == "__main__":
    unittest.main()
