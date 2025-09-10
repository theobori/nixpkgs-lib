import os
import subprocess


def which(name: str) -> bool:
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
