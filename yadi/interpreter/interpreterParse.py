__author__ = 'Manuel'
from pyparsing import *

class InterpreterException(Exception):
    pass

class IntParse:
    def parse_command(self, cmd_str):

        assert_dl = Literal("/assert ") + Word(printables)
        loadfile = Literal("/script ") + dblQuotedString + StringEnd()
        quit = Literal("/quit")
        help = Literal("/help")
        clrscr = Literal("/clrscr")
        dbs = Literal("/dbschema")

        rule = (assert_dl | loadfile | help | quit | clrscr | dbs).setFailAction(self.syntax)
        expression = rule.parseString(cmd_str)
        return expression

    def syntax(self, s, loc, expr, err):
        x = "Command {0!r} does not exist.".format(s)
        raise InterpreterException(x)
