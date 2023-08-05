"""Template commands that are oftentimes useful"""

import pash.misc
from pash.command import Command
from typing import List

def clear(cmd: Command, args: List[str]) -> None:
    """Uses pash.misc.clear to clear the console"""
    pash.misc.clear()