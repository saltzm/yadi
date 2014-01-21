from .TranslationWrapper.translateDatalogToSQL import translateDatalogToSql
from .evaluate_query import *

def start():
    while True:
        prompt = 'yadi> '
        line = input ('yadi> ')
        sql_queries = translateDatalogToSql(line)
        for s in sql_queries:
            try:
                evaluateQuery().evaluate(s)
            except Exception as e:
                print(e)
start()
