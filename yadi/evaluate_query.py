__author__ = 'nishara'



from sqlalchemy import *
from tabulate import tabulate
#TODO: allow db choice
engine = create_engine('postgresql://yadi_user:@localhost:5432/cinema', echo=True)


class evaluateQuery():
    def evaluate(self,query_to_evaluate):
        r = engine.execute(query_to_evaluate)
        fetched_results = r.fetchall()
        print (tabulate(fetched_results, tablefmt="grid"))
