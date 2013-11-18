from .safetyChecker import *
from .preprocessor import *
from .sqlFactory import *

class QueryExecutor():
    def execute_query(self, query):
        print('Original query before processing: ' + str(query))
        new_query = QueryPreprocessor().preprocess(query)
        print('Info:')
        print('Query transformed into: ' + str(new_query))
        SafetyChecker().check_for_safety(new_query)

        #print ('Processing: \n' + str(new_query))
        sql = SQLGenerator().get_SQL_code(new_query,query)
        return sql
