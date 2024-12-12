"""progress script"""

import subprocess
import os
import re
import builtins

from argparse import ArgumentParser
from typing import List, Dict
from sys import stderr, argv

from beautifultable import BeautifulTable

import nixpkgs_lib_python

from .. import fixed_points
from .. import lists


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


# Nix name -> Python name
NIX_ATTR_NAMES = {
    "fixedPoints": "fixed_points",
    "lists": "lists",
}

BUILTIN_NAMES = filter_attributes(dir(builtins))

TABLE_TITLES = ["Nix name", "Python name", "Implemented"]


def which(name):
    """_summary_

    Args:
        name (_type_): _description_

    Returns:
        _type_: _description_
    """

    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        return False

    return True


class NixpkgsLib:
    """_summary_"""

    def __init__(self, attr_names: Dict[str, str]):
        if which("nix") is False:
            print("Missing the Nix command", file=stderr)
            exit(1)

        self.__attr_names = attr_names

    @property
    def attr_names(self) -> Dict[str, str]:
        return self.__attr_names

    def __nix_expr(self, name: str) -> str:
        expr = """
        let
          pkgs = import <nixpkgs> {};
          inherit (pkgs) lib;
        in
        lib.attrNames lib.%s
        """

        return expr % (name,)

    def __nix_eval(self, expr: str) -> str:
        expr = 'nix-instantiate --eval --expr "' + expr + '"'

        stdout = subprocess.Popen(
            expr, shell=True, stdout=subprocess.PIPE
        ).stdout.read()

        return str(stdout)

    def names(self, attr_name: str) -> List[str]:
        """Returns a list of Nix names withing `lib.<attr_name>`_summary_

        Args:
            attr_name (str): _description_

        Returns:
            List[str]: _description_
        """

        expr = self.__nix_expr(attr_name)
        result = self.__nix_eval(expr)
        result = result[3:-4].strip().replace('"', "").replace("\\", "")

        return result.split()

    @staticmethod
    def python_names(nix_names: str) -> List[str]:
        """_summary_

        Args:
            nix_names (str): _description_

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

        for lib_attr in NIX_ATTR_NAMES:
            d = {}
            # Get names within lib.<name>
            nix_names = self.names(lib_attr)
            # Get the Python formatted name equivalent
            python_names = NixpkgsLib.python_names(nix_names)

            # Check if it is present in the modules names
            for nix_name, python_name in zip(nix_names, python_names):
                d[nix_name] = {
                    "python_name": python_name,
                    "implemented": python_name in module_names,
                }

            out[lib_attr] = d

        return out


def build_progress() -> Dict[str, dict]:
    """_summary_

    Returns:
        Dict[str, dict]: _description_
    """

    # Get the implemented function Python names
    module_names = []

    for module in (
        fixed_points,
        lists,
    ):
        names = dir(module)
        # Removing dunders method, just by prevention
        names = filter_attributes(names)

        module_names.extend(names)

    nix_lib = NixpkgsLib(NIX_ATTR_NAMES)

    return nix_lib.implemented_names(module_names)


def ascii_table(progress: Dict[str, dict]):
    """_summary_

    Args:
        progress (Dict[str, dict]): _description_
    """

    for attr_name, d in progress.items():
        print(attr_name)

        table = BeautifulTable()
        table.columns.header = TABLE_TITLES

        for nix_name, stats in d.items():
            table.rows.append([nix_name, stats["python_name"], stats["implemented"]])

        print(table)
        print()


def markdown_table(progress: Dict[str, dict]) -> str:
    """_summary_

    Args:
        progress (Dict[str, dict]): _description_

    Returns:
        str: _description_
    """

    out = []

    titles = "|" + "|".join(TABLE_TITLES) + "|"

    for attr_name, d in progress.items():
        table = []
        # Header row
        table.append(titles)
        # Separator
        table.append("|" + "|".join(list("-" * len(TABLE_TITLES))) + "|")

        total, implemented = 0, 0
        for nix_name, stats in d.items():
            table.append(
                "|"
                + "|".join(
                    [
                        "`" + nix_name + "`",
                        "`" + stats["python_name"] + "`",
                        "Yes" if stats["implemented"] is True else "No",
                    ]
                )
                + "|"
            )
            implemented += int(stats["implemented"])
            total += 1

        ratio = implemented / total * 100
        header_three = f"### `{attr_name}`: {ratio:.2f}% ({implemented}/{total})"

        out.append(header_three)
        out.extend(table)

        out.append("")

    return "\n".join(out)


def readme_file(progress: Dict[str, dict], template_path: str) -> str:
    """Returns a processed/subtituted README template

    Args:
        progress (Dict[str, dict]): _description_
        template_path (str): _description_

    Returns:
        str: _description_
    """

    with open(template_path) as f:
        template = f.read()

    markdown = markdown_table(progress)

    total, implemented = 0, 0

    for attr_name, d in progress.items():
        for nix_name, stats in d.items():
            if stats["implemented"] is True:
                implemented += 1
            total += 1

    ratio = implemented / total * 100
    ratio = f"{ratio:.2f}"

    return (
        template.replace("{{ progression_table }}", markdown)
        .replace("{{ progression_implemented }}", str(implemented))
        .replace("{{ progression_total }}", str(total))
        .replace("{{ progression_ratio }}", ratio)
    )


def build_argument_parser() -> ArgumentParser:
    """_summary_

    Returns:
        ArgumentParser: _description_
    """
    parser = ArgumentParser(
        prog="show-progress",
        description="CLI printing the Nixpkgs library Python implementation progress",
    )

    parser.add_argument("action", help="['ascii', 'markdown', 'readme']")
    parser.add_argument(
        "--readme-template",
        type=str,
        help="The README file template used to generate a README markdown file with the 'readme' action",
        default="./TEMPLATE.md",
    )

    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args()

    progress = build_progress()

    match args.action:
        case "ascii":
            ascii_table(progress)
        case "markdown":
            print(markdown_table(progress))
        case "readme":
            print(readme_file(progress, args.readme_template))
        case _:
            print("Unknown action", file=stderr)
            exit(1)
