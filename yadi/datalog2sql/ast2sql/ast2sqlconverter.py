from .safety_checker import *
from .preprocessor import *
from .sql_generator import *
from ...interpreter.syntax_highlighter import SyntaxHighlight


class Ast2SqlConverter():
    def convertAst2Sql(self, query):
        print('Original query before processing: ' + \
               SyntaxHighlight().highlight(str(query)), end="")

        # Preprocess the query
        new_query = QueryPreprocessor().preprocess(query)
        print('Query transformed into: ' + SyntaxHighlight().highlight(str(new_query)))

        # Check the safety of the query. Throws an exception if not safe
        SafetyChecker().check_for_safety(new_query)

        # Generates sql code from the preprocessed query
        sql = SQLGenerator().get_SQL_code(new_query,query)
        return sql
