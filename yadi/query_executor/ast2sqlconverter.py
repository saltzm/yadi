from .safetyChecker import *
from .preprocessor import *
from .sqlFactory import *
from ..interpreter.syntaxHighlighter import SyntaxHighlight


class Ast2SqlConverter():
    def convertAst2Sql(self, query):
        print('Original query before processing: ' + \
               SyntaxHighlight().highlight(str(query)), end="")
        new_query = QueryPreprocessor().preprocess(query)
        print('Query transformed into: ' + SyntaxHighlight().highlight(str(new_query)))
        SafetyChecker().check_for_safety(new_query)

        #print ('Processing: \n' + str(new_query))
        sql = SQLGenerator().get_SQL_code(new_query,query)
        return sql
