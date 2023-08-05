"""The actual command classes"""

from __future__ import annotations
import re
from typing import Union, List, Callable, Any, Tuple, Dict, Optional
from argparse import ArgumentParser

def _def_callback(cmd: Command, args: List[str]) -> None:
    """Default callback for any command (if no other callback is provided)."""
    pass

class Command(object):
    """
    Represents an actual command, something the user can enter into the shell.

    ...

    Attributes
    ----------
    aliases : List[str]
        A list of all the keywords (aliases) that the command has; that will trigger it.
    case_sensitive : bool
        Whether or not the command should respond to both the upper- and lowercase 
        versions of its aliases.
    callback : Callable[..., None]
        The function that will be called, when the command is executed.
    help : str
        A short summary of what the command does.
    cbargs : Union[Tuple[()], Tuple[Any]]
        Positional arguments that will be passed to the callback function.
    cbkwargs : Dict[str, Any]
        Keyword arguments that will be passed to the callback function.
    parent : Command
        The command's supercommand (needed for tracing).

    Methods
    -------
    matches(args)
        Checks whether or not the command should be triggered by the given cl arguments.
    trace(cu=None)
        Computes the command trace. The chain of supercommands that is needed to trigger this command.
    usage()
        Returns a short summary of this commands arguments and trace.
    __call__()
        Will call the specified callback function.
    __str__()
        Returns a nicely formatted, short help string for the command.
    """
    def __init__(self, cmd: str, 
                       *aliases: str, 
                       case_sensitive: bool = True, 
                       callback: Callable[..., None] = _def_callback, 
                       hint: str = '', 
                       cbargs: Union[Tuple[()], Tuple[Any]] = (), 
                       cbkwargs: Optional[Dict[str, Any]] = None, 
                       parent: Optional[Command] = None
                ) -> None:
        """
        Parameters
        ----------
        cmd : str
            The main keyword that will trigger this commands.
        *aliases : str
            Aliases for the main keyword.
        case_sensitive : bool
            Whether or not the lower-, upper- and mixedcase versions of the aliases should be acceptable.
            Default is True.
        callback : Callable[..., None]
            The function that will be called when this command is triggerd.
            Default is _def_callback.
        hint : str
            The short description (will be help)
            Default is ''.
        cbargs : Union[Tuple[()], Tuple[Any]]
            A tuple of positional arguments that will be passed to the callback.
            Default is ().
        cbkwargs : Optional[Dict[str, Any]]
            A dictionary of keyword arguments that will be passed to the callback.
            Default is None.
        parent : Optional[Command]
            The command's supercommand.
            Default is None.
        """
        self.aliases: List[str] = [cmd, *aliases]
        self.case_sensitive: bool = case_sensitive
        self.callback: Callable[..., None] = callback
        self.help: str = hint
        self.cbargs: Union[Tuple[()], Tuple[Any]] = cbargs
        self.cbkwargs: Dict[str, Any] = cbkwargs or dict()
        self.parent: Command = parent
        self.parser = ArgumentParser()

    def add_arg(self, *args, **kwargs) -> None:
        self.parser.add_argument(*args, **kwargs)

    def matches(self, args: Union[str, List[str]]) -> bool:
        """
        Checks whether or not the command should be triggered by the given cl arguments.
        
        ...

        Parameters
        ----------
        args : Union[str, List[str]]
            Either the commandline or the already split arguments.

        Returns
        -------
        bool
            Whether or not the command should be executed.
        """
        cmd: str = (args[0] if isinstance(args, list) else args.split()[0]).strip()
        return cmd in self.aliases or (cmd.lower() in [a.lower() for a in self.aliases] and not self.case_sensitive)

    def trace(self, cu: Optional[Command] = None) -> str:
        """
        Will compute and return the command's trace.

        Recursively goes through the supercommands until it reaches the shell;
        returns the resulting trace.

        Parameters
        ----------
        cu : Optional[Command]
            Since it's recursive - the current command.
            Default is None

        Returns
        -------
        str
            The trace (chain of keywords) needed to trigger the command.
        """
        c = cu
        if not c:
            c = self
        return (self.trace(c.parent) if c.parent else '') + c.aliases[0] + (' ' if cu else '')

    def usage(self) -> str:
        """Will return how to use the command."""
        return self.trace() + ' ' + self.parser.format_help()[self.parser.format_help().index('['):]

    def __call__(self, args: Union[str, List[str]]) -> None:
        """Will call the callback function."""
        try:
            ar = self.parser.parse_args(args if isinstance(args, list) else args.split())
        except SystemExit:
            print(self.usage())
            return
        self.callback(self, args if isinstance(args, list) else args.split(), *self.cbargs, **self.cbkwargs, **vars(ar))

    def __str__(self) -> str:
        """Returns a nicely formatted help-string."""
        return self.aliases[0] + '\t' + self.help

def _def_unkown_key(cc: CascCommand, cmdline: str) -> None:
    """The default callback for an unknown key."""
    print('Usage: %s' % cc.usage())

class CascCommand(Command):
    """
    Represents a cascading-command; a command with sub-commands.

    ...

    Attributes
    ----------
    cmds : List[Command]
        A list of all availabe sub-commands.
    sep : str
        The argument separator.
    unknown_key : Callable[[CascCommand, str], None]
        The function that will be called, if an unknown sub-command is encountered.

    Methods
    -------
    parse(cmdline)
        Parses the cmdline; checks which sub-command should be called. 
    add_cmd(cmd)
        Adds a command to its list of sub-commands.
    usage()
        Will return a trace to the command + all sub-commands summarized.
    """
    def __init__(self, cmd: str,
                       *aliases: str,
                       cmds: Optional[List[Command]] = None, 
                       case_sensitive: bool = True,
                       unknown_key: Callable[[CascCommand, str], None] = _def_unkown_key, 
                       callback: Callable[..., None] = _def_unkown_key, 
                       hint: str = '',
                       cbargs: Union[Tuple[()], Tuple[Any]] = (), 
                       cbkwargs: Optional[Dict[str, Any]] = None, 
                       parent: Optional[Command] = None,
                       sep: str = r'\s(?:(?=(?:[^"]*"[^"]*")+[^"]*$)|(?=[^"]*$))',
                ) -> None:
        """
        Parameters
        ----------
        cmd : str
            The main keyword to trigger this command.
        *aliases : str
            The main keyword's aliases; will also trigger the command.
        cmds : Optional[List[Command]]
            A list of all available sub-commands.
            Default is None.
        case_sensitive : bool
            Whether or not the keywords should be case-sensitive.
            Default is True.
        unknown_key : Callable[[CascCommand, str], None]
            The function to-be-called if an unknown sub-command is encountered.
            Default is _def_unknown_key.
        callback : Callable[..., None]
            The function that should be called upon the command's execution.
            Default is _def_unknown_key.
        hint : str
            A short summary of the command's functionality & purpose.
            Default is ''.
        cbargs : Union[Tuple[()], Tuple[Any]]
            Positional arguments that will be passed to the callback.
            Default is ().
        cbkwargs : Optional[Dict[str, Any]]
            Keyword arguments that will be passed to the callback.
            Default is None.
        parent : Optional[Command]
            The parent of the casc-command; its supercommand.
            Default is None.
        sep : str
            The argument separator.
            Default is r'\s(?:(?=(?:[^"]*"[^"]*")+[^"]*$)|(?=[^"]*$))'.
        """
        super().__init__(cmd, *aliases, callback=callback, case_sensitive=case_sensitive, hint=hint, cbargs=cbargs, cbkwargs=cbkwargs, parent=parent)
        self.cmds: List[Command] = cmds or []
        self.unknown_key: Callable[[CascCommand, str], None] = unknown_key
        self.sep: str = sep
        for c in self.cmds:
            c.parent = self

    def parse(self, cmdline: str) -> None:
        """
        Parses the cmdline; checks what to do with it.

        Calls the appropriate sub-commands, etc.

        Parameters
        ----------
        cmdline : str
            Not the actual complete cmdline, but the cmdline after the argument
            that triggered this command.
        """
        if not cmdline.strip():
            self('')
            return
        c: List[Command] = list(filter(lambda c: c.matches(cmdline), self.cmds))
        if not c:
            self.unknown_key(self, cmdline)
            return
        args = re.split(self.sep, cmdline)[1:]
        if isinstance(c[0], CascCommand):
            c[0].parse(' '.join(args))
            return
        c[0]([a.replace('"', '') for a in args])

    def add_cmd(self, cmd: Command) -> None:
        """Adds a command to the sub-commands list."""
        cmd.parent = self
        self.cmds.append(cmd)

    def usage(self) -> str:
        """Returns the trace + options to use with this command."""
        t: str = self.trace()
        return '{} [{}]'.format(t, '|'.join([c.trace().replace(t+' ', '') for c in self.cmds]))
