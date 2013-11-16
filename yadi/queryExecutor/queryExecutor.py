from safetyChecker import *
from preprocessor import *
from sqlFactory import *

class QueryExecutor():
    def execute_query(self, query):
        new_query = QueryPreprocessor().preprocess(query)
        print 'Minified query ' + str(new_query)
        try:
            SafetyChecker().check_for_safety(new_query)        
        except SafetyException as e:
            return str(e)
        sql = SQLGenerator().get_SQL_code(new_query,query)
        return sql
