"""Test fixed points module"""

import unittest

from nixpkgs_lib import (
    fix,
    fix_prime,
    extends,
    converge,
    to_extension,
    elem_at,
    compose_extensions,
    compose_many_extensions,
    make_extensible,
)


class TestFixedPoints(unittest.TestCase):
    """Controller for the fixed point tests"""

    def atest_fixed_points_fix_dict(self):
        """Test fixed points with a dict"""

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

    def atest_fixed_points_fix_list(self):
        """Test fixed points with a list"""

        it_function = lambda self: [
            "hello",
            self[0] + " world " + elem_at(self)(0),
            self[1] + "world",
            self[0] == "hello",
        ]

        it = fix(it_function)

        self.assertEqual(it[1], "hello world hello")

    def atest_fixed_points_extends(self):
        """Test fixed points extends function"""

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

    def atest_fixed_points_converge(self):
        """Test fixed points converge function"""
        result = converge(lambda x: x // 2, 16)

        self.assertEqual(result, 0)

    def atest_fixed_points_to_extension(self):
        """Test fixed points to_extension function"""

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

    def atest_fixed_points_compose_many_extensions(self):
        """Test fixed points compose_many_extensions function"""

        original = lambda final: {"a": 1}

        overlay_a = lambda final: lambda prev: {"b": final["c"], "c": 3}
        overlay_b = lambda final: lambda prev: {"c": 10, "x": prev["c"] or 5}

        extensions = compose_many_extensions([overlay_a, overlay_b])

        fixed_point = fix(extends(extensions)(original))

        self.assertEqual(fixed_point, {"a": 1, "b": 10, "c": 10, "x": 3})

    def atest_fixed_points_make_extensible(self):
        """Test fixed points make_extensible function"""

        obj = make_extensible(lambda final: {})

        obj = obj["extend"](lambda final: lambda prev: {"foo": "foo"})

        self.assertEqual(obj["foo"], "foo")

        obj = obj["extend"](
            lambda final: lambda prev: {
                "foo": prev["foo"] + " + ",
                "bar": "bar",
                "foobar": final["foo"] + final["bar"],
            }
        )

        self.assertEqual(obj["foo"], "foo + ")
        self.assertEqual(obj["foobar"], "foo + bar")


if __name__ == "__main__":
    unittest.main()
