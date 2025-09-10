"""test lists module"""

import unittest

from nixpkgs_lib.lists import (
    foldr,
    foldl,
    _all,
    all_unique,
    _any,
    imap0,
    imap1,
    ifilter0,
    flatten,
    remove,
    find_single,
    find_first,
    _range,
    replicate,
    partition,
    group_by,
    group_by_prime,
    zip_lists_with,
    zip_lists,
    reverse_list,
    compare_lists,
    natural_sort,
    has_prefix,
    remove_prefix,
    sublist,
    common_prefix,
    init,
    intersect_lists,
    subtract_lists,
    mutually_exclusive,
    foldl_prime,
    count,
    take,
    take_end,
    unique,
    sort,
    sort_on,
    concat_map,
    cross_lists,
    list_dfs,
    toposort,
    drop,
    drop_end,
    unique_strings,
)


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

        result = foldl_prime(lambda acc: lambda x: acc + x)(0)([1, 2, 3])

        self.assertEqual(result, 6)

    def test_lists_all(self):
        """Test lists all"""

        result = _all(lambda x: x % 2 == 0)((2, 4, 6, 8))

        self.assertTrue(result)

    def test_lists_all_unique(self):
        """Test lists all unique"""

        self.assertFalse(all_unique([3, 2, 3, 4]))
        self.assertTrue(all_unique([3, 2, 4, 1]))

    def test_lists_any(self):
        """Test lists all unique"""

        self.assertTrue(_any(lambda x: type(x) is str)([1, "a", {}]))
        self.assertFalse(_any(lambda x: type(x) is str)([1, {}]))

    def test_lists_imap0(self):
        """Test lists imap0"""

        result = imap0(lambda i: lambda x: f"{x}-{i}", ["a", "b"])
        self.assertEqual(result, ["a-0", "b-1"])

    def test_lists_imap1(self):
        """Test lists imap1"""

        result = imap1(lambda i: lambda x: f"{x}-{i}", ["a", "b"])
        self.assertEqual(result, ["a-1", "b-2"])

    def test_lists_ifilter0(self):
        """Test lists ifilter0"""

        result = ifilter0(lambda i: lambda x: i == 0 or x > 2)([1, 2, 3])
        self.assertEqual(result, [1, 3])

    def test_lists_flatten(self):
        """Test lists flatten"""

        result1 = flatten([1, [2, [3], 4], 5])
        result2 = flatten(1)

        self.assertEqual(result1, [1, 2, 3, 4, 5])
        self.assertEqual(result2, [1])

    def test_lists_remove(self):
        """Test lists remove"""

        result = remove(3, [1, 3, 4, 3])
        self.assertEqual(result, [1, 4])

    def test_lists_find_single(self):
        """Test lists find_single"""

        result1 = find_single(lambda x: x == 3, "none", "multiple", [1, 3, 3])
        result2 = find_single(lambda x: x == 3, "none", "multiple", [1, 3])
        result3 = find_single(lambda x: x == 3, "none", "multiple", [1, 9])

        self.assertEqual(result1, "multiple")
        self.assertEqual(result2, 3)
        self.assertEqual(result3, "none")

    def test_lists_find_first(self):
        """Test lists find_first"""

        result1 = find_first(lambda x: x > 3, 7, [1, 6, 4])
        result2 = find_first(lambda x: x > 9, 7, [1, 6, 4])

        self.assertEqual(result1, 6)
        self.assertEqual(result2, 7)

    def test_lists_range(self):
        """Test lists range"""

        self.assertEqual(_range(2, 4), [2, 3, 4])
        self.assertEqual(_range(3, 2), [])

    def test_lists_replicate(self):
        """Test lists replicate"""

        self.assertEqual(replicate(3, "a"), ["a", "a", "a"])
        self.assertEqual(replicate(2, True), [True, True])

    def test_lists_partition(self):
        """Test lists partition"""

        result = partition(lambda x: x > 2, [5, 1, 2, 3, 4])
        self.assertEqual(result["right"], [5, 3, 4])
        self.assertEqual(result["wrong"], [1, 2])

    def test_lists_group_by(self):
        """Test lists group_by"""

        data = [
            {"name": "icewm", "script": "icewm &"},
            {"name": "xfce", "script": "xfce4-session &"},
            {"name": "icewm", "script": "icewmbg &"},
        ]
        result = group_by(lambda x: x["name"], data)
        self.assertEqual(len(result["icewm"]), 2)
        self.assertEqual(len(result["xfce"]), 1)

    def test_lists_group_by_prime(self):
        """Test lists group_by_prime"""

        result = group_by_prime(
            lambda acc, x: acc + x, 0, lambda x: str(x > 2), [5, 1, 2, 3, 4]
        )
        self.assertEqual(result["True"], 12)
        self.assertEqual(result["False"], 3)

    def test_lists_zip_lists_with(self):
        """Test lists zip_lists_with"""

        result = zip_lists_with(lambda a, b: f"{a}{b}", ["h", "l"], ["e", "o"])
        self.assertEqual(result, ["he", "lo"])

    def test_lists_zip_lists(self):
        """Test lists zip_lists"""

        result = zip_lists([1, 2], ["a", "b"])
        self.assertEqual(result, [{"fst": 1, "snd": "a"}, {"fst": 2, "snd": "b"}])

    def test_lists_reverse_list(self):
        """Test lists reverse_list"""

        self.assertEqual(reverse_list(["b", "o", "j"]), ["j", "o", "b"])

    def test_lists_list_dfs(self):
        """Test lists list_dfs"""

        pass

    def test_lists_toposort(self):
        """Test lists toposort"""

        pass

    def test_lists_compare_lists(self):
        """Test lists compare_lists"""

        self.assertEqual(compare_lists(lambda a, b: (a > b) - (a < b), [], []), 0)
        self.assertEqual(compare_lists(lambda a, b: (a > b) - (a < b), [], ["a"]), -1)
        self.assertEqual(compare_lists(lambda a, b: (a > b) - (a < b), ["a"], []), 1)
        self.assertEqual(
            compare_lists(lambda a, b: (a > b) - (a < b), ["a", "b"], ["a", "c"]), -1
        )

    def test_lists_natural_sort(self):
        """Test lists natural_sort"""

        self.assertEqual(
            natural_sort(["disk11", "disk8", "disk100", "disk9"]),
            ["disk8", "disk9", "disk11", "disk100"],
        )
        self.assertEqual(
            natural_sort(["v0.2", "v0.15", "v0.0.9"]), ["v0.0.9", "v0.2", "v0.15"]
        )

    def test_lists_has_prefix(self):
        """Test lists has_prefix"""

        self.assertTrue(has_prefix([1, 2], [1, 2, 3, 4]))
        self.assertFalse(has_prefix([0, 1], [1, 2, 3, 4]))

    def test_lists_remove_prefix(self):
        """Test lists remove_prefix"""

        self.assertEqual(remove_prefix([1, 2], [1, 2, 3, 4]), [3, 4])
        with self.assertRaises(ValueError):
            remove_prefix([0, 1], [1, 2, 3, 4])

    def test_lists_sublist(self):
        """Test lists sublist"""

        self.assertEqual(sublist(1, 3, ["a", "b", "c", "d", "e"]), ["b", "c", "d"])
        self.assertEqual(sublist(1, 3, []), [])

    def test_lists_common_prefix(self):
        """Test lists common_prefix"""

        self.assertEqual(common_prefix([1, 2, 3, 4, 5, 6], [1, 2, 4, 8]), [1, 2])
        self.assertEqual(common_prefix([1, 2, 3], [4, 5, 6]), [])

    def test_lists_init(self):
        """Test lists init"""

        self.assertEqual(init([1, 2, 3]), [1, 2])
        with self.assertRaises(ValueError):
            init([])

    def test_lists_intersect_lists(self):
        """Test lists intersect_lists"""

        self.assertEqual(intersect_lists([1, 2, 3], [6, 3, 2]), [3, 2])

    def test_lists_subtract_lists(self):
        """Test lists subtract_lists"""

        self.assertEqual(subtract_lists([3, 2], [1, 2, 3, 4, 5, 3]), [1, 4, 5])

    def test_lists_mutually_exclusive(self):
        """Test lists mutually_exclusive"""

        self.assertTrue(mutually_exclusive([], [1, 2, 3]))
        self.assertTrue(mutually_exclusive([4, 5, 6], [1, 2, 3]))
        self.assertFalse(mutually_exclusive([1, 2, 3], [3, 4, 5]))

    def test_lists_count(self):
        """Test lists count"""

        result = count(lambda x: x == 3)([3, 2, 3, 4, 6])

        self.assertEqual(result, 2)

    def test_lists_take(self):
        """Test lists take"""

        result = take(2)(["a", "b", "c", "d"])

        self.assertEqual(result, ["a", "b"])
        self.assertEqual(take(2)([]), [])

    def test_lists_take(self):
        """Test lists take"""

        result = take_end(2)(["a", "b", "c", "d"])

        self.assertEqual(result, ["c", "d"])
        self.assertEqual(take(2)([]), [])

    def test_lists_unique(self):
        """Test lists unique"""

        self.assertEqual(unique([3, 2, 3, 4]), [3, 2, 4])

    def test_lists_sort(self):
        """Test lists sort"""

        f = lambda p: lambda q: p - q
        result = sort(f)([5, 3, 7])

        self.assertEqual(result, [3, 5, 7])

    def test_lists_sort_on(self):
        """Test lists sort_on"""

        result = sort_on(len)(["aa", "b", "cccc"])

        self.assertEqual(result, ["b", "aa", "cccc"])

    def test_lists_concat_map(self):
        """Test lists concat_map"""

        result = concat_map(lambda x: [x] + ["z"])(["a", "b"])

        self.assertEqual(result, ["a", "z", "b", "z"])

    def test_lists_cross_lists(self):
        """Test lists cross_lists"""

        f = lambda x: lambda y: x + y
        result = cross_lists(f)([[1, 2], [3, 4]])

        self.assertEqual(result, [4, 5, 5, 6])

    def test_lists_list_dfs(self):
        """Test lists listtest_lists_list_dfs"""

        result = list_dfs(True)(has_prefix)(["/home/user", "other", "/", "/home"])
        self.assertEqual(
            result,
            {
                "minimal": "/",
                "visited": ["/home/user"],
                "rest": ["/home", "other"],
            },
        )

        result = list_dfs(True)(has_prefix)(["/home/user", "other", "/", "/home", "/"])
        self.assertEqual(
            result,
            {
                "cycle": "/",
                "loops": ["/"],
                "visited": ["/", "/home/user"],
                "rest": ["/home", "other"],
            },
        )

    def test_lists_toposort(self):
        """Test lists listtest_lists_toposort"""

        result = toposort(has_prefix)(["/home/user", "other", "/", "/home"])
        self.assertEqual(result, {"result": ["/", "/home", "/home/user", "other"]})

        result = toposort(has_prefix)(["/home/user", "other", "/", "/home", "/"])
        self.assertEqual(result, {"cycle": ["/home/user", "/", "/"], "loops": ["/"]})

        result = toposort(has_prefix)(["other", "/home/user", "/home", "/"])
        self.assertEqual(result, {"result": ["other", "/", "/home", "/home/user"]})

        result = toposort(lambda a: lambda b: a < b)([3, 2, 1])
        self.assertEqual(result, {"result": [1, 2, 3]})

    def test_lists_drop(self):
        """Test lists drop"""

        result = drop(2, ["a", "b", "c", "d"])

        self.assertEqual(result, ["c", "d"])

    def test_lists_drop_end(self):
        """Test lists drop_end"""

        result = drop_end(2, ["a", "b", "c", "d"])

        self.assertEqual(result, ["a", "b"])

    def test_lists_unique_strings(self):
        """Test lists unique_strings"""

        result = unique_strings(["foo", "bar", "foo"])

        self.assertEqual(result, ["foo", "bar"])


if __name__ == "__main__":
    unittest.main()
