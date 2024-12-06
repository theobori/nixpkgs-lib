"""test fixed point module"""

import unittest

from nixpkgs_lib_python import fix, fix_prime, extends


class TestFixedPoint(unittest.TestCase):
    """Controller for the fixed point tests"""

    def test_fixed_point_fix_dict(self):
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

    def test_fixed_point_fix_list(self):
        """Test fixed point with a list"""

        it_function = lambda self: [
            "hello",
            self[0] + " world " + self[0],
            self[1] + "world",
            self[0] == "hello",
        ]

        it = fix(it_function)

        self.assertEqual(it[1], "hello world hello")

    def test_fixed_point_extends(self):
        """Test fixed point extends function"""

        f = lambda final: {"a": 1, "b": final["a"] + 2}

        overlay = lambda final, prev: {"a": prev["a"] + 10}
        result = fix(extends(overlay, f))

        self.assertEqual(result, {"a": 11, "b": 13})

        overlay = lambda final, prev: {"b": final["a"] + 5}
        result = fix(extends(overlay, f))

        self.assertEqual(result, {"a": 1, "b": 6})

        overlay = lambda final, prev: {"c": prev["a"] + final["b"]}
        result = fix(extends(overlay, f))

        self.assertEqual(result, {"a": 1, "b": 3, "c": 4})

    # def test_fixed_point_compose_extensions(self):
    #     """Test fixed point extends function"""

    #     original = lambda final: {"a": 1}

    #     overlay_a = lambda final, prev: {"b": final["c"], "c": 3}
    #     overlay_b = lambda final, prev: {"c": 10, "x": prev["c"] or 5}


if __name__ == "__main__":
    unittest.main()
