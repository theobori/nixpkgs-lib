"""progress script"""

from argparse import ArgumentParser
from typing import Dict, NoReturn, Callable, Tuple, Any
from sys import stderr, exit

from beautifultable import BeautifulTable

from nixpkgs_lib import fixed_points
from nixpkgs_lib import lists
from nixpkgs_lib import strings

from nixpkgs_lib._nix import NixProgress, filter_attributes

TABLE_TITLES = ["Nix name", "Python name", "Implemented"]


def build_progress(filter_func: Callable, modules: tuple) -> Dict[str, dict]:
    """_summary_

    Args:
        filter_func (Callable): _description_

    Returns:
        Dict[str, dict]: _description_
    """

    # Get the implemented function Python names
    module_names = set()

    for module in modules:
        names = dir(module)
        # Removing dunders method, just by prevention
        names = filter_func(names)

        module_names |= set(names)

    nix = NixProgress()

    return nix.implemented_names(module_names)


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

    parser.add_argument("action", choices=["ascii", "markdown", "readme"])
    parser.add_argument(
        "--readme-template-file",
        type=str,
        help="The README file template used to generate a README markdown file with the 'readme' action",
        default="./TEMPLATE.md",
        required=False,
    )

    return parser


def print_fatal(*args: Tuple[str], **kwargs: Dict[str, Any]):
    """Calls the print function with custom arguments and
    redirection to the standard error stream.

    Then it exit the program with status code 1.
    """

    print(*args, **kwargs, file=stderr)
    exit(1)


def main() -> NoReturn:
    parser = build_argument_parser()
    args = parser.parse_args()

    modules = (fixed_points, lists, strings)

    progress: Dict[str, dict]
    try:
        progress = build_progress(filter_func=filter_attributes, modules=modules)
    except Exception as e:
        print_fatal(e)

    match args.action:
        case "ascii":
            ascii_table(progress)
        case "markdown":
            print(markdown_table(progress))
        case "readme":
            print(readme_file(progress, args.readme_template_file))
        case _:
            print_fatal("Unknown action")
