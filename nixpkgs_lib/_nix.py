"""nix module"""

import subprocess
import re

from typing import List, Dict, Set

from nixpkgs_lib._builtin import BUILTIN_NAMES_FILTERED

# Nix name -> Python name
NIX_ATTR_NAMES = {
    "fixedPoints": "fixed_points",
    "lists": "lists",
    "strings": "strings",
}


def nix_get_attr_names_expression(name: str) -> str:
    """Return a Nix expression to get a list of attribute names.

    Args:
        name (str): The attribute name.

    Returns:
        str: The substitued Nix expression.
    """

    expr = """
    let
        pkgs = import <nixpkgs> {};
        inherit (pkgs) lib;
    in
    lib.attrNames %s
    """

    return expr % (name,)


def nix_get_lib_attr_names_expression(lib_attr: str) -> str:
    """Return a Nix expression to get a list of attribute names of an attribute within lib.

    Args:
        name (str): The lib attribute name.

    Returns:
        str: The substitued Nix expression.
    """

    return nix_get_attr_names_expression(f"lib.{lib_attr}")


def nix_eval_expression(expr: str) -> str:
    """Evaluate a Nix expression.

    Args:
        expr (str): The Nix expression.

    Returns:
        str: The Nix expression evaluation return value.
    """

    expr = 'nix-instantiate --eval --expr "' + expr + '"'

    stdout = subprocess.Popen(expr, shell=True, stdout=subprocess.PIPE).stdout.read()

    return str(stdout)


def nix_get_lib_attr_names(attr_name: str) -> List[str]:
    """Returns a list of Nix names withing `lib.<attr_name>`_summary_

    Args:
        attr_name (str): _description_

    Returns:
        List[str]: _description_
    """

    expr = nix_get_lib_attr_names_expression(attr_name)
    result = nix_eval_expression(expr)
    result = result[3:-4].strip().replace('"', "").replace("\\", "")

    return result.split()


def get_python_names(
    nix_names: List[str], builtin_names: Set[str] = BUILTIN_NAMES_FILTERED
) -> List[str]:
    """Convert Nix name to Python name. Applying standard Python naming rules.

    Args:
        nix_names (List[str]): The Nix names.
        builtin_names (Set[str]): A set of Python builtin names.

    Returns:
        List[str]: A list of Python names.
    """

    def format_nix_name(name: str) -> str:
        # Snake case
        out = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
        # Replace ' by _prime
        out = out.replace("'", "_prime")
        # Check if the name is a builtin python name
        if out in builtin_names:
            out = "_" + out
        # Later, probably the number will be replaced with their letters name

        return out

    return list(map(format_nix_name, nix_names))


def get_implemented_names(
    module_names: List[str], attr_names: Dict[str, str] = NIX_ATTR_NAMES
) -> Dict[str, dict]:
    """_summary_

    Args:
        module_names (List[str]): _description_

    Returns:
        Dict[str, dict]: _description_
    """

    out = {}

    for lib_attr in attr_names:
        d = {}
        # Get names within lib.<name>
        nix_names = nix_get_lib_attr_names(lib_attr)
        # Get the Python formatted name equivalent
        python_names = get_python_names(nix_names)

        # Check if it is present in the modules names
        for nix_name, python_name in zip(nix_names, python_names):
            d[nix_name] = {
                "python_name": python_name,
                "implemented": python_name in module_names,
            }

        out[lib_attr] = d

    return out
