# Nixpkgs Library part implementation in Python
[![build](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This GitHub repository is a fun project whose aim is to implement in [Python](https://www.python.org/) the `lib` part of [Nixpkgs](https://github.com/NixOS/nixpkgs), more precisely the logic part. All functions implemented as part of the Nixpkgs library are [curryfied](https://en.wikipedia.org/wiki/Currying). As far as `builtins` functions are concerned, only those required by `lib` will be added to the module, and they will only be available through `lib`, i.e. `nixpkgs_lib_python`.

## Implementation progress: 58.82% (40 / 68)

This section lists all the functions in the Nixpkgs library that are supposed to be implemented.
Each function name is associated with a status indicating whether it has been implemented.

### `fixedPoints`: 55.56% (5/9)
|Nix name|Python name|Implemented|
|-|-|-|
|`composeExtensions`|`compose_extensions`|No|
|`composeManyExtensions`|`compose_many_extensions`|No|
|`converge`|`converge`|Yes|
|`extends`|`extends`|Yes|
|`fix`|`fix`|Yes|
|`fix'`|`fix_prime`|Yes|
|`makeExtensible`|`make_extensible`|No|
|`makeExtensibleWithCustomName`|`make_extensible_with_custom_name`|No|
|`toExtension`|`to_extension`|Yes|

### `lists`: 59.32% (35/59)
|Nix name|Python name|Implemented|
|-|-|-|
|`all`|`_all`|Yes|
|`allUnique`|`all_unique`|Yes|
|`any`|`_any`|Yes|
|`commonPrefix`|`common_prefix`|Yes|
|`compareLists`|`compare_lists`|Yes|
|`concatLists`|`concat_lists`|No|
|`concatMap`|`concat_map`|No|
|`count`|`count`|No|
|`crossLists`|`cross_lists`|No|
|`drop`|`drop`|No|
|`elem`|`elem`|No|
|`elemAt`|`elem_at`|No|
|`filter`|`_filter`|No|
|`findFirst`|`find_first`|Yes|
|`findFirstIndex`|`find_first_index`|No|
|`findSingle`|`find_single`|Yes|
|`flatten`|`flatten`|Yes|
|`fold`|`fold`|Yes|
|`foldl`|`foldl`|Yes|
|`foldl'`|`foldl_prime`|No|
|`foldr`|`foldr`|Yes|
|`forEach`|`for_each`|Yes|
|`genList`|`gen_list`|No|
|`groupBy`|`group_by`|Yes|
|`groupBy'`|`group_by_prime`|Yes|
|`hasPrefix`|`has_prefix`|Yes|
|`head`|`head`|Yes|
|`ifilter0`|`ifilter0`|Yes|
|`imap0`|`imap0`|Yes|
|`imap1`|`imap1`|Yes|
|`init`|`init`|Yes|
|`intersectLists`|`intersect_lists`|Yes|
|`isList`|`is_list`|No|
|`last`|`last`|No|
|`length`|`length`|No|
|`listDfs`|`list_dfs`|No|
|`map`|`_map`|No|
|`mutuallyExclusive`|`mutually_exclusive`|Yes|
|`naturalSort`|`natural_sort`|Yes|
|`optional`|`optional`|No|
|`optionals`|`optionals`|No|
|`partition`|`partition`|Yes|
|`range`|`_range`|Yes|
|`remove`|`remove`|Yes|
|`removePrefix`|`remove_prefix`|Yes|
|`replicate`|`replicate`|Yes|
|`reverseList`|`reverse_list`|Yes|
|`singleton`|`singleton`|Yes|
|`sort`|`sort`|No|
|`sortOn`|`sort_on`|No|
|`sublist`|`sublist`|Yes|
|`subtractLists`|`subtract_lists`|Yes|
|`tail`|`tail`|Yes|
|`take`|`take`|No|
|`toList`|`to_list`|No|
|`toposort`|`toposort`|No|
|`unique`|`unique`|No|
|`zipLists`|`zip_lists`|Yes|
|`zipListsWith`|`zip_lists_with`|Yes|


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
from nixpkgs_lib_python import fix

result_dict = fix(
    lambda self: {
        "a": "3",
        "b": int(self["a"]) + 1,
    }
)
result_list = fix(lambda self: ["3", int(self[0]) + 1])
```

## Contribute

If you want to help the project, you can follow the guidelines in [CONTRIBUTING.md](./CONTRIBUTING.md).

