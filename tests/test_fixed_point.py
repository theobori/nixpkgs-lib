"""test fixed point module"""

import unittest

from nixpkgs_lib_python import fix, fix_prime, extends, converge, to_extension


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

        overlay = lambda final: lambda prev: {"a": prev["a"] + 10}
        result = fix(extends(overlay, f))

        self.assertDictEqual(result, {"a": 11, "b": 13})

        overlay = lambda final: lambda prev: {"b": final["a"] + 5}
        result = fix(extends(overlay, f))

        self.assertDictEqual(result, {"a": 1, "b": 6})

        overlay = lambda final: lambda prev: {"c": prev["a"] + final["b"]}
        result = fix(extends(overlay, f))

        self.assertDictEqual(result, {"a": 1, "b": 3, "c": 4})

    def test_fixed_point_converge(self):
        """Test fixed point converge function"""
        result = converge(lambda x: x // 2, 16)

        self.assertEqual(result, 0)

    def test_fixed_point_to_extension(self):
        """Test fixed point to_extension function"""

        extension = to_extension({"a": 1, "b": 2})
        result = fix(extends(extension, lambda final: {"a": 0, "c": final["a"]}))

        self.assertDictEqual(result, {"a": 1, "b": 2, "c": 1})

        extension = to_extension(lambda prev: {"a": 1, "b": prev["a"]})
        result = fix(extends(extension, lambda final: {"a": 0, "c": final["a"]}))

        self.assertDictEqual(result, {"a": 1, "b": 0, "c": 1})

        extension = to_extension(
            lambda final: lambda prev: {"a": 1, "b": prev["a"], "c": final["a"] + 1}
        )
        result = fix(extends(extension, lambda final: {"a": 0, "c": final["a"]}))

        self.assertDictEqual(result, {"a": 1, "b": 0, "c": 2})


if __name__ == "__main__":
    unittest.main()
