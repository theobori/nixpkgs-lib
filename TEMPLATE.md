# Nixpkgs Library part implementation in Python
[![build](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml/badge.svg)](https://github.com/theobori/nixpkgs-lib-python/actions/workflows/build.yml)

[![built with nix](https://builtwithnix.org/badge.svg)](https://builtwithnix.org)

This GitHub repository is a fun project whose aim is to implement in [Python](https://www.python.org/) the `lib` part of [Nixpkgs](https://github.com/NixOS/nixpkgs), more precisely the logic part. All functions implemented as part of the Nixpkgs library are [curryfied](https://en.wikipedia.org/wiki/Currying). As far as `builtins` functions are concerned, only those required by `lib` will be added to the module, and they will only be available through `lib`, i.e. `nixpkgs_lib`.

## Implementation progress: {{ progression_ratio }}% ({{ progression_implemented }} / {{ progression_total }})

This section lists all the functions in the Nixpkgs library that are supposed to be implemented.
Each function name is associated with a status indicating whether it has been implemented.

{{ progression_table }}

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
