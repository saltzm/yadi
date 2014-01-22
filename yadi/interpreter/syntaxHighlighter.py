__author__ = 'Manuel'
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import get_formatter_by_name
import pygments


class SyntaxHighlight:
    def highlight(self, text):
        result = str(highlight(text, pygments.lexers.get_lexer_by_name("prolog"), pygments.formatters.get_formatter_by_name("terminal")))
        return result
