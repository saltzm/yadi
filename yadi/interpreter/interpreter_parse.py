__author__ = 'Manuel'
from pyparsing import *

class InterpreterException(Exception):
    pass

class IntParse:
    def parse_command(self, cmd_str):

        assert_dl = Literal("/assert ") + Word(printables)
        loadfile = Literal("/script ") + dblQuotedString + StringEnd()
        quit = Literal("/quit") + StringEnd()
        help = Literal("/help") + StringEnd()
        clrscr = Literal("/clrscr") + StringEnd()
        dbs = Literal("/dbschema") + StringEnd()
        setdb = Literal("/setdb") + StringEnd()
        curdb = Literal("/curdb") + StringEnd()
        drop = Literal("/dropview") + Word(printables)
        drop_t = Literal("/droptable") + Word(printables)

        rule = (assert_dl | loadfile | help | quit | clrscr | dbs | setdb |
                curdb | drop | drop_t).setFailAction(self.syntax)
        expression = rule.parseString(cmd_str)
        return expression

    def syntax(self, s, loc, expr, err):
        x = "Command {0!r} does not exist.".format(s)
        raise InterpreterException(x)
