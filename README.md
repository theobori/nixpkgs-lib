# Nixpkgs Library part implementation in Python
[![build](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This GitHub repository is a fun project whose aim is to implement in [Python](https://www.python.org/) the `lib` part of [Nixpkgs](https://github.com/NixOS/nixpkgs), more precisely the logic part. All functions implemented as part of the Nixpkgs library are [curryfied](https://en.wikipedia.org/wiki/Currying). As far as `builtins` functions are concerned, only those required by `lib` will be added to the module, and they will only be available through `lib`, i.e. `nixpkgs_lib`.

## Implementation progress: 97.10% (67 / 69)

This section lists all the functions in the Nixpkgs library that are supposed to be implemented.
Each function name is associated with a status indicating whether it has been implemented.

### `fixedPoints`: 100.00% (9/9)
|Nix name|Python name|Implemented|
|-|-|-|
|`composeExtensions`|`compose_extensions`|Yes|
|`composeManyExtensions`|`compose_many_extensions`|Yes|
|`converge`|`converge`|Yes|
|`extends`|`extends`|Yes|
|`fix`|`fix`|Yes|
|`fix'`|`fix_prime`|Yes|
|`makeExtensible`|`make_extensible`|Yes|
|`makeExtensibleWithCustomName`|`make_extensible_with_custom_name`|Yes|
|`toExtension`|`to_extension`|Yes|

### `lists`: 96.67% (58/60)
|Nix name|Python name|Implemented|
|-|-|-|
|`all`|`_all`|Yes|
|`allUnique`|`all_unique`|Yes|
|`any`|`_any`|Yes|
|`commonPrefix`|`common_prefix`|Yes|
|`compareLists`|`compare_lists`|Yes|
|`concatLists`|`concat_lists`|Yes|
|`concatMap`|`concat_map`|Yes|
|`count`|`count`|Yes|
|`crossLists`|`cross_lists`|Yes|
|`drop`|`drop`|Yes|
|`dropEnd`|`drop_end`|No|
|`elem`|`elem`|Yes|
|`elemAt`|`elem_at`|Yes|
|`filter`|`_filter`|Yes|
|`findFirst`|`find_first`|Yes|
|`findFirstIndex`|`find_first_index`|Yes|
|`findSingle`|`find_single`|Yes|
|`flatten`|`flatten`|Yes|
|`fold`|`fold`|Yes|
|`foldl`|`foldl`|Yes|
|`foldl'`|`foldl_prime`|Yes|
|`foldr`|`foldr`|Yes|
|`forEach`|`for_each`|Yes|
|`genList`|`gen_list`|Yes|
|`groupBy`|`group_by`|Yes|
|`groupBy'`|`group_by_prime`|Yes|
|`hasPrefix`|`has_prefix`|Yes|
|`head`|`head`|Yes|
|`ifilter0`|`ifilter0`|Yes|
|`imap0`|`imap0`|Yes|
|`imap1`|`imap1`|Yes|
|`init`|`init`|Yes|
|`intersectLists`|`intersect_lists`|Yes|
|`isList`|`is_list`|Yes|
|`last`|`last`|Yes|
|`length`|`length`|Yes|
|`listDfs`|`list_dfs`|Yes|
|`map`|`_map`|Yes|
|`mutuallyExclusive`|`mutually_exclusive`|Yes|
|`naturalSort`|`natural_sort`|Yes|
|`optional`|`optional`|Yes|
|`optionals`|`optionals`|Yes|
|`partition`|`partition`|Yes|
|`range`|`_range`|Yes|
|`remove`|`remove`|Yes|
|`removePrefix`|`remove_prefix`|Yes|
|`replicate`|`replicate`|Yes|
|`reverseList`|`reverse_list`|Yes|
|`singleton`|`singleton`|Yes|
|`sort`|`sort`|Yes|
|`sortOn`|`sort_on`|No|
|`sublist`|`sublist`|Yes|
|`subtractLists`|`subtract_lists`|Yes|
|`tail`|`tail`|Yes|
|`take`|`take`|Yes|
|`toList`|`to_list`|Yes|
|`toposort`|`toposort`|Yes|
|`unique`|`unique`|Yes|
|`zipLists`|`zip_lists`|Yes|
|`zipListsWith`|`zip_lists_with`|Yes|


## Function calling style

Technically, all functions with more than one argument are curried, so they must be called as follows.

```python
from nixpkgs_lib import find_single

find_single(lambda x: x == 3)("none")("multiple")([1, 9])
```

But in this module, the functions, although curried, can be called in any way.

```python
from nixpkgs_lib import find_single

# A more comfortable calling style, still returning a function that return a function
first_part = find_single(lambda x: x == 3, "none")
# More explicit calling style
first_part("multiple")([1, 9])
```

## Example

Here's a simple example of what can be done with this module.

The Nix version.
```nix
let
  pkgs = import <nixpkgs> { };
  inherit (pkgs.lib) fix toInt elemAt;
in
{
  resultAttrset = fix (self: {
    a = "3";
    b = (toInt self.a) + 1;
  });
  resultList = fix (self: [
    "3"
    ((toInt (elemAt self 0)) + 1)
  ]);
}
```

The Python version.
```python
from nixpkgs_lib import fix, elem_at

result_dict = fix(
    lambda self: {
        "a": "3",
        "b": int(self["a"]) + 1,
    }
)
result_list = fix(lambda self: ["3", int(elem_at(self)(0)) + 1])
```

## Contribute

If you want to help the project, you can follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

