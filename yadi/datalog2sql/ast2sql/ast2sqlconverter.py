from .safety_checker import *
from .preprocessor import *
from .sql_generator import *
from ...sql_engine.db_state_tracker import DBStateTracker
from ...interpreter.syntax_highlighter import SyntaxHighlight

class Ast2SqlConverter:
    def __init__(self, db_state_tracker):
        self.db_state_tracker = db_state_tracker

    def convertAst2Sql(self, query):
        print('Original query before processing: ' + \
               SyntaxHighlight().highlight(str(query)), end="")

        # Preprocess the query
        new_query = QueryPreprocessor().preprocess(query)
        print('Query transformed into: ' + SyntaxHighlight().highlight(str(new_query)))

        # Check the safety of the query. Throws an exception if not safe
        SafetyChecker().check_for_safety(new_query)

        # Generates sql code from the preprocessed query
        sql = SQLGenerator(self.db_state_tracker).get_SQL_code(new_query,query)
        return sql
