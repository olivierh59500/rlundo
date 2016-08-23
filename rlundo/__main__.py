#!/usr/bin/env python

"""
rlundo

Start a repl with undo.
"""

from __future__ import unicode_literals
import sys
import os
import argparse

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import rlundo

from rlundo.rlundoable import modify_env_with_modified_rl
from rlundo.termrewrite import run_with_listeners

from rlundo import interps


def start_undoable_rl(interpreter, interparg):
    """Run an interpreter either with an undo script or with a generic method.

    If an interpreter matches the first argument, run script like that.
    Otherwise run that command in an environment where a modified readline will
    be used instead of the standard one."""
    for command, predicate in interps.interpreters:
        if predicate(interpreter):
            return run_with_listeners(command + interparg)
    else:
        modify_env_with_modified_rl()
        return run_with_listeners([interpreter] + interparg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='accepting an interpreter and any interpreter arguments into rlundo')
    parser.add_argument('interpreter', metavar='I', help='command to call the interpreter')
    parser.add_argument('interparg', nargs=argparse.REMAINDER, help='any arguments you can feed into the interpreter')
    argobject = parser.parse_args()
    start_undoable_rl(argobject.interpreter, argobject.interparg)
