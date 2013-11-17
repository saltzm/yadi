__author__ = 'nishara'



from sqlalchemy import *
from tabulate import tabulate
engine = create_engine('postgresql://postgres:123456@localhost:5432/Cinema', echo=True)


class evaluateQuery():
    def evaluate(self,query_to_evaluate):
        r = engine.execute(query_to_evaluate)
        fetched_results = r.fetchall()
        print tabulate(fetched_results, tablefmt="grid")