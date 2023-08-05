Convenience functions for working with the Cmd module
and other command line related stuff.

*Latest release 20200615*:
BaseCommand.usage_text: do not mention the "help" command if it is the only subcommand (it won't be available if there are no other subcommands).

## Class `BaseCommand`

A base class for handling nestable command lines.

This class provides the basic parse and dispatch mechanisms
for command lines.
To implement a command line
one instantiates a subclass of BaseCommand:

    class MyCommand(BaseCommand):
      GETOPT_SPEC = 'ab:c'
      USAGE_FORMAT = r"""Usage: {cmd} [-a] [-b bvalue] [-c] [--] arguments...
        -a    Do it all.
        -b    But using bvalue.
        -c    The 'c' option!
      """
    ...
    the_cmd = MyCommand()

Running a command is done by:

    the_cmd.run(argv)

The subclass is customised by overriding the following methods:
* `apply_defaults(options)`:
  prepare the initial state of `options`
  before any command line options are applied
* `apply_opts(options,opts)`:
  apply the `opts` to `options`.
  `opts` is an `(option,value)` sequence
  as returned by `getopot.getopt`.
* `cmd_`*subcmd*`(argv,options)`:
  if the command line options are followed by an argument
  whose value is *subcmd*,
  then the method `cmd_`*subcmd*`(argv,options)`
  will be called where `argv` contains the command line arguments
  after *subcmd*.
* `main(argv,options)`:
  if there are no command line aguments after the options
  or the first argument does not have a corresponding
  `cmd_`*subcmd* method
  then method `main(argv,options)`
  will be called where `argv` contains the command line arguments.
* `run_context(argv,options,cmd)`:
  a context manager to provide setup or teardown actions
  to occur before and after the command implementation respectively.
  If the implementation is a `cmd_`*subcmd* method
  then this is called with `cmd=`*subcmd*;
  if the implementation is `main`
  then this is called with `cmd=None`.

To aid recursive use
it is intended that all the per command state
is contained in the `options` object
and therefore that in typical use
all of `apply_opts`, `cmd_`*subcmd*, `main` and `run_context`
should be static methods making no reference to `self`.

Editorial: why not arparse?
Primarily because when incorrectly invoked
an argparse command line prints the help/usage messgae
and aborts the whole programme with `SystemExit`.

## Function `docmd(dofunc)`

Decorator for Cmd subclass methods
to supply some basic quality of service.

This decorator:
- wraps the function call in a `cs.pfx.Pfx` for context
- intercepts `getopt.GetoptError`s, issues a `warning`
  and runs `self.do_help` with the method name,
  then returns `None`
- intercepts other `Exception`s,
  issues an `exception` log message
  and returns `None`

The intended use is to decorate `cmd.Cmd` `do_`* methods:

    from cmd import Cmd
    class MyCmd(Cmd):
      @docmd
      def do_something(...):
        ... do something ...

# Release Log



*Release 20200615*:
BaseCommand.usage_text: do not mention the "help" command if it is the only subcommand (it won't be available if there are no other subcommands).

*Release 20200521.1*:
Fix DISTINFO.install_requires.

*Release 20200521*:
* BaseCommand.run: support using BaseCommand subclasses as cmd_* names to make it easy to nest BaseCommands.
* BaseCommand: new hack_postopts_argv method called after parsing the main command line options, for inferring subcommands or the like.
* BaseCommand: extract "Usage:" paragraphs from subcommand method docstrings to build the main usage message.
* BaseCommand: new cmd_help default command.
* Assorted bugfixes and small improvements.

*Release 20200318*:
* BaseCommand.run: make argv optional, get additional usage keywords from self.USAGE_KEYWORDS.
* @BaseCommand.add_usage_to_docstring: honour cls.USAGE_KEYWORDS.
* BaseCommand: do not require GETOPT_SPEC for commands with no defined options.
* BaseCommand.run: call cs.logutils.setup_logging.

*Release 20200229*:
Improve subcommand selection logic, replace StackableValues with stackattrs, drop `cmd` from arguments passed to main/cmd_* methods (present in `options`).

*Release 20200210*:
* New BaseCommand.add_usage_to_docstring class method to be called after class setup, to append the usage message to the class docstring.
* BaseCommand.run: remove spurious Pfx(cmd), as logutils does this for us already.

*Release 20190729*:
BaseCommand: support for a USAGE_FORMAT usage message format string and a getopt_error_handler method.

*Release 20190619.1*:
Another niggling docstring formatting fix.

*Release 20190619*:
Minor documentation updates.

*Release 20190617.2*:
Lint.

*Release 20190617.1*:
Initial release with @docmd decorator and alpha quality BaseCommand command line assistance class.
