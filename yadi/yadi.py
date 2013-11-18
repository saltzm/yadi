from .TranslationWrapper.translateDatalogToSQL import translateDatalogToSql
from .evaluate_query import *

def start():
    while True:
        line = input ('yadi> ')
        s = translateDatalogToSql(line)
        evaluateQuery().evaluate(s[0])
start()
