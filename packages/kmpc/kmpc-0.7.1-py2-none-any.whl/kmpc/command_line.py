import argparse
import sys
from kmpc.extra import KmpcHelpers, SmartStdout, set_defaultencoding_globally

from kmpc.version import VERSION_STR

parser = argparse.ArgumentParser()
parser.add_argument(
        "-q", "--quiet",
        help="only print errors to console log",
        action="store_true")
parser.add_argument(
        "-d", "--debug",
        help="print debug messages to console log",
        action="store_true")
parser.add_argument(
        "-n", "--newconfig",
        help="write out default config file if it doesn't exist yet",
        action="store_true")
parser.add_argument(
        "-V", "--version",
        help="print version number and exit",
        action="store_true")
parser.add_argument(
        "--helpkivy",
        help="Print Kivy's built-in argument list",
        action="store_true")
parser.add_argument(
        "--sync",
        help="run the 'sync' function with the chosen module and exit",
        choices=['all', 'music',
                 'cache', 'exportratings',
                 'importratings'])


def do_args(dodebug=False):
    # since kivy has it's own argparsing, it's necessary to do some argv
    # mangling
    args, unknown = parser.parse_known_args()
    sys.argv[1:] = unknown
    # if --helpkivy is passed, print Kivy's argument list
    if args.helpkivy:
        sys.argv.append('-h')
    # if -d/--debug is passed, use Kivy's -d flag
    if args.debug or dodebug:
        sys.argv.append('-d')
    if args.version:
        print sys.argv[0]+" v"+VERSION_STR
        sys.exit(0)
    from kivy.config import Config
    if args.quiet:
        Config.set('kivy', 'log_level', 'warning')
    return args


def main_app(dodebug=False):
    sys.stdout = sys.stderr = SmartStdout()
    set_defaultencoding_globally('utf-8')
    args = do_args(dodebug)
    from kmpc import kmpcapp
    kmpcapp.KmpcApp(args).run()

