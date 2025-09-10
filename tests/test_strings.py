"""test strings module"""

import unittest

from nixpkgs_lib.strings import (
    to_upper,
    char_to_int,
    cmake_bool,
    cmake_feature,
    cmake_option_type,
    common_prefix_length,
    common_suffix_length,
    concat_imap_strings,
    concat_imap_strings_sep,
    concat_lines,
    concat_map_attrs_string_sep,
    concat_map_strings,
    concat_map_strings_sep,
    concat_strings,
    concat_strings_sep,
    enable_feature,
    enable_feature_as,
)


class TestStrings(unittest.TestCase):
    """Controller for the strings tests"""

    def test_to_upper(self):
        """Test strings to_upper"""

        self.assertEqual(to_upper("abcXYZ"), "ABCXYZ")
        self.assertEqual(to_upper("déjà vu"), "DÉJÀ VU")

    def test_char_to_int(self):
        """Test strings char_to_int"""

        self.assertEqual(char_to_int("A"), ord("A"))
        self.assertEqual(char_to_int("é"), ord("é"))

    def test_cmake_option_type(self):
        """Test strings cmake_option_type"""

        self.assertEqual(
            cmake_option_type("BOOL", "WITH_TESTS", "TRUE"), "-DWITH_TESTS:BOOL=TRUE"
        )
        self.assertEqual(cmake_option_type("string", "FOO", "bar"), "-DFOO:STRING=bar")
        self.assertEqual(cmake_option_type("Path", "ROOT", "/x"), "-DROOT:PATH=/x")
        with self.assertRaises(AssertionError):
            cmake_option_type("UNKNOWN", "X", "Y")

    def test_cmake_bool(self):
        """Test strings cmake_bool"""

        self.assertEqual(cmake_bool("WITH_SSL", True), "-DWITH_SSL:BOOL=TRUE")
        self.assertEqual(cmake_bool("WITH_SSL", False), "-DWITH_SSL:BOOL=FALSE")

    def test_cmake_feature(self):
        """Test strings cmake_feature"""

        self.assertEqual(
            cmake_feature("CMAKE_BUILD_TYPE", "Release"),
            "-DCMAKE_BUILD_TYPE:STRING=Release",
        )

    def test_common_prefix_length(self):
        """Test strings common_prefix_length"""

        self.assertEqual(common_prefix_length("foobar", "foobaz"), 5)
        self.assertEqual(common_prefix_length("abc", "xyz"), 0)
        self.assertEqual(common_prefix_length("", "abc"), 0)
        self.assertEqual(common_prefix_length("abc", ""), 0)
        self.assertEqual(common_prefix_length("same", "same"), 4)

    def test_common_suffix_length(self):
        """Test strings common_suffix_length"""

        self.assertEqual(common_suffix_length("foobar", "quxbar"), 3)
        self.assertEqual(common_suffix_length("abc", "xyz"), 0)
        self.assertEqual(common_suffix_length("", "abc"), 0)
        self.assertEqual(common_suffix_length("abc", ""), 0)
        self.assertEqual(common_suffix_length("same", "same"), 4)

    def test_concat_strings_sep(self):
        """Test strings concat_strings_sep"""

        self.assertEqual(concat_strings_sep(",", ["a", "b", "c"]), "a,b,c")
        self.assertEqual(concat_strings_sep(",", []), "")

    def test_concat_strings(self):
        """Test strings concat_strings"""

        self.assertEqual(concat_strings(["a", "b", "c"]), "abc")
        self.assertEqual(concat_strings([]), "")

    def test_concat_lines(self):
        """Test strings concat_lines"""

        self.assertEqual(concat_lines(["a", "b", "c"]), "a\nb\nc")
        self.assertEqual(concat_lines([]), "")

    def test_concat_map_strings_sep(self):
        """Test strings concat_map_strings_sep"""

        f = lambda s: f"<{s}>"
        self.assertEqual(concat_map_strings_sep(",", f, ["a", "b"]), "<a>,<b>")
        self.assertEqual(concat_map_strings_sep(",", f, []), "")

    def test_concat_map_strings(self):
        """Test strings concat_map_strings"""

        f = lambda s: f"[{s}]"
        self.assertEqual(concat_map_strings(f, ["a", "b"]), "[a][b]")
        self.assertEqual(concat_map_strings(f, []), "")

    def test_concat_imap_strings(self):
        """Test strings concat_imap_strings"""

        f = lambda i: lambda s: f"{s}{i}"
        self.assertEqual(concat_imap_strings(f, ["a", "b"]), "a1b2")
        self.assertEqual(concat_imap_strings(f, []), "")

    def test_concat_imap_strings_sep(self):
        """Test strings concat_imap_strings_sep"""

        f = lambda i: lambda s: f"{s}{i}"
        self.assertEqual(concat_imap_strings_sep(",", f, ["a", "b"]), "a1,b2")
        self.assertEqual(concat_imap_strings_sep(",", f, []), "")

    def test_concat_map_attrs_string_sep(self):
        """Test strings concat_map_attrs_string_sep"""

        attrs = {"a": "1", "b": "2"}
        f = lambda name, value: f"{name}={value}"
        self.assertEqual(concat_map_attrs_string_sep(", ", f, attrs), "a=1, b=2")
        self.assertEqual(concat_map_attrs_string_sep(", ", f, {}), "")

    def test_enable_feature(self):
        """Test strings enable_feature"""

        self.assertEqual(enable_feature(True, "ssl"), "--enable-ssl")
        self.assertEqual(enable_feature(False, "ssl"), "--disable-ssl")

    def test_enable_feature_as(self):
        """Test strings enable_feature_as"""

        self.assertEqual(
            enable_feature_as(True, "feature", "value"), "--enable-feature=value"
        )
        self.assertEqual(
            enable_feature_as(False, "feature", "value"), "--disable-feature"
        )


if __name__ == "__main__":
    unittest.main()
