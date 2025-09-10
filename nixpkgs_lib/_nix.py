import subprocess
import re
import builtins

from typing import List, Dict

from nixpkgs_lib._command import which


def filter_attributes(names: List[str]) -> List[str]:
    """Filter Python attributes, keeping only snake_case string

    Args:
        names (List[str]): Attributes

    Returns:
        List[str]: Filtered attributes
    """

    return list(
        filter(
            lambda name: not (
                (name.startswith("__") and name.endswith("__")) or name[0].isupper()
            ),
            names,
        )
    )


BUILTIN_NAMES = set(filter_attributes(dir(builtins)))

# Nix name -> Python name
NIX_ATTR_NAMES = {
    "fixedPoints": "fixed_points",
    "lists": "lists",
    "strings": "strings",
}


class Nix:
    """_summary_"""

    def __init__(self):
        if which("nix") is False:
            raise OSError("Missing the Nix command")

    def attr_names_expression(self, name: str) -> str:
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

    def lib_attr_names_expression(self, lib_attr: str) -> str:
        """Return a Nix expression to get a list of attribute names of an attribute within lib.

        Args:
            name (str): The lib attribute name.

        Returns:
            str: The substitued Nix expression.
        """

        return self.attr_names_expression(f"lib.{lib_attr}")

    def eval_nix_expression(self, expr: str) -> str:
        """Evaluate a Nix expression.

        Args:
            expr (str): The Nix expression.

        Returns:
            str: The Nix expression evaluation return value.
        """

        expr = 'nix-instantiate --eval --expr "' + expr + '"'

        stdout = subprocess.Popen(
            expr, shell=True, stdout=subprocess.PIPE
        ).stdout.read()

        return str(stdout)


class NixProgress(Nix):
    """Implementation progress controller"""

    def __init__(self, attr_names: Dict[str, str] = NIX_ATTR_NAMES):
        super().__init__()

        self.__attr_names = attr_names

    @property
    def attr_names(self) -> Dict[str, str]:
        return self.__attr_names

    def names(self, attr_name: str) -> List[str]:
        """Returns a list of Nix names withing `lib.<attr_name>`_summary_

        Args:
            attr_name (str): _description_

        Returns:
            List[str]: _description_
        """

        expr = self.lib_attr_names_expression(attr_name)
        result = self.eval_nix_expression(expr)
        result = result[3:-4].strip().replace('"', "").replace("\\", "")

        return result.split()

    @staticmethod
    def python_names(nix_names: List[str]) -> List[str]:
        """_summary_

        Args:
            nix_names (List[str]): _description_

        Returns:
            List[str]: _description_
        """

        def format_nix_name(name: str) -> str:
            # Snake case
            out = re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()
            # Replace ' by _prime
            out = out.replace("'", "_prime")
            # Check if the name is a builtin python name
            if out in BUILTIN_NAMES:
                out = "_" + out
            # Later, probably the number will be replaced with their letters name

            return out

        return list(map(format_nix_name, nix_names))

    def implemented_names(self, module_names: List[str]) -> Dict[str, dict]:
        """_summary_

        Args:
            module_names (List[str]): _description_

        Returns:
            Dict[str, dict]: _description_
        """

        out = {}

        for lib_attr in self.__attr_names:
            d = {}
            # Get names within lib.<name>
            nix_names = self.names(lib_attr)
            # Get the Python formatted name equivalent
            python_names = NixProgress.python_names(nix_names)

            # Check if it is present in the modules names
            for nix_name, python_name in zip(nix_names, python_names):
                d[nix_name] = {
                    "python_name": python_name,
                    "implemented": python_name in module_names,
                }

            out[lib_attr] = d

        return out
