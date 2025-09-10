"""strings module"""

from string import ascii_uppercase

from nixpkgs_lib._curry import curry

upper_chars = ascii_uppercase


def to_upper(s: str) -> str:
    """Transform each character of the string to uppercase"""

    return s.upper()
