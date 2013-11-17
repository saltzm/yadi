__author__ = 'saltzm'

from sqlalchemy import *
from tabulate import tabulate
import os
engine = create_engine('postgresql://yadi_user:@localhost:5432/twitter', echo=True)


def create_db():
    with open(os.path.join(os.path.dirname(__file__), 'database_creation/setup.sql'), 'r') as content_file:
        content = content_file.read()
    r = engine.execute(content)
    fetched_results = r.fetchall()
    print (tabulate(fetched_results, tablefmt="grid"))
create_db()
