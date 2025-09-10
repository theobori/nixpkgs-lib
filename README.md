# Nixpkgs Library part implementation in Python
[![build](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This GitHub repository is a fun project whose aim is to implement in [Python](https://www.python.org/) the `lib` part of [Nixpkgs](https://github.com/NixOS/nixpkgs), more precisely the logic part. All functions implemented as part of the Nixpkgs library are [curryfied](https://en.wikipedia.org/wiki/Currying). As far as `builtins` functions are concerned, only those required by `lib` will be added to the module, and they will only be available through `lib`, i.e. `nixpkgs_lib`.

## Implementation progress: 47.16% (83 / 176)

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

### `lists`: 100.00% (62/62)
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
|`dropEnd`|`drop_end`|Yes|
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
|`sortOn`|`sort_on`|Yes|
|`sublist`|`sublist`|Yes|
|`subtractLists`|`subtract_lists`|Yes|
|`tail`|`tail`|Yes|
|`take`|`take`|Yes|
|`takeEnd`|`take_end`|Yes|
|`toList`|`to_list`|Yes|
|`toposort`|`toposort`|Yes|
|`unique`|`unique`|Yes|
|`uniqueStrings`|`unique_strings`|Yes|
|`zipLists`|`zip_lists`|Yes|
|`zipListsWith`|`zip_lists_with`|Yes|

### `strings`: 11.43% (12/105)
|Nix name|Python name|Implemented|
|-|-|-|
|`addContextFrom`|`add_context_from`|No|
|`charToInt`|`char_to_int`|No|
|`cmakeBool`|`cmake_bool`|No|
|`cmakeFeature`|`cmake_feature`|No|
|`cmakeOptionType`|`cmake_option_type`|No|
|`commonPrefixLength`|`common_prefix_length`|No|
|`commonSuffixLength`|`common_suffix_length`|No|
|`compareVersions`|`compare_versions`|No|
|`concatImapStrings`|`concat_imap_strings`|No|
|`concatImapStringsSep`|`concat_imap_strings_sep`|No|
|`concatLines`|`concat_lines`|No|
|`concatMapAttrsStringSep`|`concat_map_attrs_string_sep`|No|
|`concatMapStrings`|`concat_map_strings`|No|
|`concatMapStringsSep`|`concat_map_strings_sep`|No|
|`concatStrings`|`concat_strings`|No|
|`concatStringsSep`|`concat_strings_sep`|No|
|`elem`|`elem`|Yes|
|`elemAt`|`elem_at`|Yes|
|`enableFeature`|`enable_feature`|No|
|`enableFeatureAs`|`enable_feature_as`|No|
|`escape`|`escape`|No|
|`escapeC`|`escape_c`|No|
|`escapeNixIdentifier`|`escape_nix_identifier`|No|
|`escapeNixString`|`escape_nix_string`|No|
|`escapeRegex`|`escape_regex`|No|
|`escapeShellArg`|`escape_shell_arg`|No|
|`escapeShellArgs`|`escape_shell_args`|No|
|`escapeURL`|`escape_u_r_l`|No|
|`escapeXML`|`escape_x_m_l`|No|
|`fileContents`|`file_contents`|No|
|`filter`|`_filter`|Yes|
|`fixedWidthNumber`|`fixed_width_number`|No|
|`fixedWidthString`|`fixed_width_string`|No|
|`floatToString`|`float_to_string`|No|
|`fromJSON`|`from_j_s_o_n`|No|
|`genList`|`gen_list`|Yes|
|`getName`|`get_name`|No|
|`getVersion`|`get_version`|No|
|`hasInfix`|`has_infix`|No|
|`hasPrefix`|`has_prefix`|Yes|
|`hasSuffix`|`has_suffix`|No|
|`head`|`head`|Yes|
|`intersperse`|`intersperse`|No|
|`isAttrs`|`is_attrs`|No|
|`isCoercibleToString`|`is_coercible_to_string`|No|
|`isConvertibleWithToString`|`is_convertible_with_to_string`|No|
|`isInt`|`is_int`|No|
|`isList`|`is_list`|Yes|
|`isPath`|`is_path`|No|
|`isStorePath`|`is_store_path`|No|
|`isString`|`is_string`|No|
|`isStringLike`|`is_string_like`|No|
|`isValidPosixName`|`is_valid_posix_name`|No|
|`levenshtein`|`levenshtein`|No|
|`levenshteinAtMost`|`levenshtein_at_most`|No|
|`lowerChars`|`lower_chars`|No|
|`makeBinPath`|`make_bin_path`|No|
|`makeIncludePath`|`make_include_path`|No|
|`makeLibraryPath`|`make_library_path`|No|
|`makeSearchPath`|`make_search_path`|No|
|`makeSearchPathOutput`|`make_search_path_output`|No|
|`match`|`match`|No|
|`mesonBool`|`meson_bool`|No|
|`mesonEnable`|`meson_enable`|No|
|`mesonOption`|`meson_option`|No|
|`nameFromURL`|`name_from_u_r_l`|No|
|`normalizePath`|`normalize_path`|No|
|`optionalString`|`optional_string`|No|
|`parseDrvName`|`parse_drv_name`|No|
|`readFile`|`read_file`|No|
|`readPathsFromFile`|`read_paths_from_file`|No|
|`removePrefix`|`remove_prefix`|Yes|
|`removeSuffix`|`remove_suffix`|No|
|`replaceChars`|`replace_chars`|No|
|`replaceString`|`replace_string`|No|
|`replaceStrings`|`replace_strings`|No|
|`replicate`|`replicate`|Yes|
|`sanitizeDerivationName`|`sanitize_derivation_name`|No|
|`split`|`split`|No|
|`splitString`|`split_string`|No|
|`splitStringBy`|`split_string_by`|No|
|`storeDir`|`store_dir`|No|
|`stringAsChars`|`string_as_chars`|No|
|`stringLength`|`string_length`|No|
|`stringToCharacters`|`string_to_characters`|No|
|`substring`|`substring`|No|
|`tail`|`tail`|Yes|
|`toCamelCase`|`to_camel_case`|No|
|`toInt`|`to_int`|No|
|`toIntBase10`|`to_int_base10`|No|
|`toJSON`|`to_j_s_o_n`|No|
|`toLower`|`to_lower`|No|
|`toSentenceCase`|`to_sentence_case`|No|
|`toShellVar`|`to_shell_var`|No|
|`toShellVars`|`to_shell_vars`|No|
|`toUpper`|`to_upper`|Yes|
|`trim`|`trim`|No|
|`trimWith`|`trim_with`|No|
|`typeOf`|`type_of`|No|
|`unsafeDiscardStringContext`|`unsafe_discard_string_context`|No|
|`upperChars`|`upper_chars`|Yes|
|`versionAtLeast`|`version_at_least`|No|
|`versionOlder`|`version_older`|No|
|`withFeature`|`with_feature`|No|
|`withFeatureAs`|`with_feature_as`|No|


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

