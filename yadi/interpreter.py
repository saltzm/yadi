from .translateDatalogToSQL import translateDatalogToSql
from .evaluate_query import *

while True:
    line = input ('yadi> ')
    s = translateDatalogToSql(line)
    evaluateQuery().evaluate(s[0])
