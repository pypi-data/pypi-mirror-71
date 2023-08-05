from __future__ import annotations
from typing import Union, List, Optional

class Keyword(object):
    def __init__(self, kw: str, *aliases: str, case_sensitive: bool = True, hint: str = '', parent: Optional[Keyword] = None):
        self._aliases: List[str] = [kw, *aliases]
        self._case_sensitive: bool = case_sensitive
        self._help: str = hint
        self.parent = parent

    def matches(self, args: Union[str, List[str]]) -> bool:
        cmd: str = (args[0] if isinstance(args, list) else args.split()[0]).strip()
        return cmd in self._aliases or (cmd.lower() in [a.lower() for a in self._aliases] and not self._case_sensitive)

    def help(self) -> str:
        return self._help

    def trace(self, cu: Optional[Keyword] = None) -> str:
        c = cu
        if not c:
            c = self
        return (self.trace(c.parent) if c.parent else '') + c._aliases[0] + (' ' if cu else '')

    def usage(self) -> str:
        return self.trace()

    def __str__(self) -> str:
        return '{}\t{}'.format(self._aliases[0], self.help())