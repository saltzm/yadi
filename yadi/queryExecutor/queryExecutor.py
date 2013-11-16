from .safetyChecker import *
from .preprocessor import *
from .sqlFactory import *

class QueryExecutor():
    def execute_query(self, query):        
        try:
            new_query = QueryPreprocessor().preprocess(query)
            SafetyChecker().check_for_safety(new_query)        
        except SafetyException as e:
            return str(e)
        print ('Processing: \n' + str(new_query))
        sql = SQLGenerator().get_SQL_code(new_query,query)
        return sql
