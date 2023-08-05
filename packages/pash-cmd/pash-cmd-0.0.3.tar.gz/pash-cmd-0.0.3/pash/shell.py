"""Home to the pash shell and its default functions."""

from __future__ import annotations
import pash.misc as misc
from pash.command import Command, CascCommand
from typing import List, Callable, Union

def _def_unknown_cmd(cc: CascCommand, cmdline: str) -> None:
    """Default callback for unknown commands"""
    if not cmdline.strip():
        return
    print('Unknown command "%s" ... ' % cmdline.split()[0])

class Shell(CascCommand):
    """
    The class representing the actual shell the user interacts with.

    ...

    Attributes
    ----------
    prompt : str
        The shell's prompt (the string prefixing the user's input; e.g.: 'bernd@raspberrypi: ').
    __interrupt_end : bool
        Whether or not the shell should terminate when a `KeyboardInterrupt` exception (Ctrl+C) arises.
    __exited : bool
        Whether or not the shell has terminated yet.
    helpc : CascCommand
        The `help` command. It takes care of calls to 'help' and '?'.

    Methods
    -------
    exit()
        Terminates the shell. (__exited = True)
    add_cmd(cmd)
        Adds a command the terminal will respond to.
    prompt_until_exit()
        Keep asking the user for input and handling those commands, until the shell terminates.
    print_help()
        Print all possible commands and their short help summary.
    """
    def __init__(self, prompt: str = '$ ', 
                       interrupt_end: bool = False, 
                       unknown_cmd: Callable[[CascCommand, str], None] = _def_unknown_cmd,
                       sep: str = r'\s(?:(?=(?:[^"]*"[^"]*")+[^"]*$)|(?=[^"]*$))'
                ) -> None:
        """
        Parameters
        ----------
        prompt : str
            The shell's prompt.
            Default is '$ '.
        interrupt_end : bool
            Whether or not the shell should terminate on a KeyboardInterrupt.
            Default is False.
        unknown_cmd : Callable[[CascCommand, str], None]
            The function that will be called, when the shell encounters an unknown command.
            Default is _def_unknown_cmd.
        sep : str
            The argument separator.
            Default is r'\s(?:(?=(?:[^"]*"[^"]*")+[^"]*$)|(?=[^"]*$))'.
        """
        super().__init__('', unknown_key=unknown_cmd, sep=sep)
        self.__interrupt_end: bool = interrupt_end
        self.__exited: bool = False
        self.prompt: str = prompt
        self.helpc: CascCommand = CascCommand('help', '?', callback=lambda c, a: self.print_help(), hint='Displays help for any/all commands ...')
        self.add_cmd(self.helpc)

    def exit(self) -> None:
        """Terminates the shell"""
        self.__exited = True

    def add_cmd(self, cmd: Command) -> None:
        """
        Adds a command to the shell.

        ...

        Parameters
        ----------
        cmd : Command
            The command to-be-added.
        """
        self.cmds.append(cmd)
        self.helpc.add_cmd(Command(*cmd.aliases, 
            case_sensitive=cmd.case_sensitive, 
            callback=lambda c, a: print(' Usage: ' + cmd.usage()+'\n Aliases: '+', '.join(cmd.aliases)+'\n Help: '+cmd.help)))

    def prompt_until_exit(self) -> None:
        """Keeps prompting the user for more input (commands) until the shell terminates."""
        self.__exited = False
        while not self.__exited:
            try:
                print(self.prompt, end='')
                cmdline: str = input()
                self.parse(cmdline)
            except KeyboardInterrupt:
                print()
                if self.__interrupt_end:
                    self.__exited = True
                    break
    
    def print_help(self) -> None:
        """Prints all available commands and their short help summaries."""
        misc.print_table([[ str(c).split('\t')[0], str(c).split('\t')[1], ] for c in self.cmds], align=misc.TALIGN.LEFT)

    def __call__(self, args: Union[str, List[str]]) -> None:
        """Does nothing - overrides parent."""
        return