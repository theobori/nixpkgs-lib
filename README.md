# Nixpkgs Library part implementation in Python
[![build](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This GitHub repository is a fun project whose aim is to implement in [Python](https://www.python.org/) the `lib` part of [Nixpkgs](https://github.com/NixOS/nixpkgs), more precisely the logic part. All functions implemented as part of the Nixpkgs library are [curryfied](https://en.wikipedia.org/wiki/Currying). As far as `builtins` functions are concerned, only those required by `lib` will be added to the module, and they will only be available through `lib`, i.e. `nixpkgs_lib_python`.

## Implementation progress: 14.71% (10 / 68)

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

### `lists`: 8.47% (5/59)
|Nix name|Python name|Implemented|
|-|-|-|
|`all`|`all`|No|
|`allUnique`|`all_unique`|No|
|`any`|`any`|No|
|`commonPrefix`|`common_prefix`|No|
|`compareLists`|`compare_lists`|No|
|`concatLists`|`concat_lists`|No|
|`concatMap`|`concat_map`|No|
|`count`|`count`|No|
|`crossLists`|`cross_lists`|No|
|`drop`|`drop`|No|
|`elem`|`elem`|No|
|`elemAt`|`elem_at`|No|
|`filter`|`filter`|No|
|`findFirst`|`find_first`|No|
|`findFirstIndex`|`find_first_index`|No|
|`findSingle`|`find_single`|No|
|`flatten`|`flatten`|No|
|`fold`|`fold`|Yes|
|`foldl`|`foldl`|Yes|
|`foldl'`|`foldl_prime`|No|
|`foldr`|`foldr`|Yes|
|`forEach`|`for_each`|Yes|
|`genList`|`gen_list`|No|
|`groupBy`|`group_by`|No|
|`groupBy'`|`group_by_prime`|No|
|`hasPrefix`|`has_prefix`|No|
|`head`|`head`|No|
|`ifilter0`|`ifilter0`|No|
|`imap0`|`imap0`|No|
|`imap1`|`imap1`|No|
|`init`|`init`|No|
|`intersectLists`|`intersect_lists`|No|
|`isList`|`is_list`|No|
|`last`|`last`|No|
|`length`|`length`|No|
|`listDfs`|`list_dfs`|No|
|`map`|`map`|No|
|`mutuallyExclusive`|`mutually_exclusive`|No|
|`naturalSort`|`natural_sort`|No|
|`optional`|`optional`|No|
|`optionals`|`optionals`|No|
|`partition`|`partition`|No|
|`range`|`range`|No|
|`remove`|`remove`|No|
|`removePrefix`|`remove_prefix`|No|
|`replicate`|`replicate`|No|
|`reverseList`|`reverse_list`|No|
|`singleton`|`singleton`|Yes|
|`sort`|`sort`|No|
|`sortOn`|`sort_on`|No|
|`sublist`|`sublist`|No|
|`subtractLists`|`subtract_lists`|No|
|`tail`|`tail`|No|
|`take`|`take`|No|
|`toList`|`to_list`|No|
|`toposort`|`toposort`|No|
|`unique`|`unique`|No|
|`zipLists`|`zip_lists`|No|
|`zipListsWith`|`zip_lists_with`|No|


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

