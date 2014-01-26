__author__ = 'nishara','Manuel'

from sqlalchemy import *
from sqlalchemy.engine import reflection
from tabulate import tabulate
from colorama import *
import os
import logging

class QueryEvaluator:
    # The typical usage of create_engine() is once per particular database URL, held globally for the
    # lifetime of a single application process. A single Engine manages many individual DBAPI connections on behalf
    # of the process and is intended to be called upon in a concurrent fashion. In other words, the object shouldn't
    # be changed but we can have as many engines as we need. See:
    # http://stackoverflow.com/questions/11366294/sqlalchemy-engine-multiple-databases-with-mysql
    engine_list = []
    connection = None

    def initialize_db(self):
        x = ""
        logging.basicConfig()
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        try:
            with open(os.path.join(os.path.dirname(__file__),
                'dbconf.txt'), 'r') as f:
                x = f.readline()
                self.engine_list.append(create_engine(x, echo=False))
            return True
        except Exception as e:
            print(Fore.RED+"Cannot read dbconf.txt file, please set a DB configuration using /setdb"+Fore.RESET)
            self.engine_list.append(create_engine("postgresql://empty:empty@empty:0000/db", echo=False))
            return False

    def dispose_last(self):
        self.engine_list[-1].dispose()

        #This condition checks that, if the user still didn't attempt to evaluate any query
        #and he wants to change the close YADI, then the connection object would still be None. So, no need to close
        #the connection in that scenario.
        if self.connection is not None:
            self.connection.close()

    def get_schema(self):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
        try:
            inspector = reflection.Inspector.from_engine(self.engine_list[-1])
            table_names = inspector.get_table_names()
            column_names = []

            for i in range(0, len(table_names)):
                column_names.append(inspector.get_columns(table_names[i]))

            print(Fore.GREEN+'Relation information:')
            for i in range(0, len(table_names)):
                print(table_names[i]+'(', end="")
                for j in range(0, len(column_names[i])):
                    print(column_names[i][j].get('name')+':'+str(column_names[i][j].get('type')), end="")
                    if j is not len(column_names[i])-1:
                        print(", ", end="")
                print(")\n")
            print(Fore.RESET)
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        except Exception as e:
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
            print(Fore.RED+"Error while retrieving schema: "+str(e)+Fore.RESET)


    def saveconf(self):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'dbconf.txt'), 'w') as f:
                str_parse = str(self.engine_list[-1])
                new = str_parse[len("Engine("):-len(")")]
                f.write(new)
        except Exception as e:
            pass

    def set_engine(self, urlstring):
        self.engine_list[-1].dispose()

        #Same remark as on dispose_last()
        if self.connection is not None:
            self.connection.close()

        try:
            print("Verifying validity of: "+urlstring)
            test_engine = create_engine(urlstring, echo=False)
            test_connection = test_engine.connect()
            test_connection.close()
            test_engine.dispose()
            self.engine_list.append(create_engine(urlstring, echo=False))
            print(Fore.GREEN+"Settings saved."+Fore.RESET)
        except Exception as e:
            print(Fore.RED+"Unsuccessful connection: "+str(e)+Fore.RESET)

    def print_engine_url(self):
        print(str(self.engine_list[-1]), end="")

    def evaluate(self, query_to_evaluate):
        self.connection = self.engine_list[-1].connect()
        r = self.connection.execute(query_to_evaluate)
        fetched_results = r.fetchall()
        grid_string = tabulate(fetched_results, tablefmt="grid")
        print(grid_string)

    def execute(self, query_to_evaluate):
        self.connection = self.engine_list[-1].connect()
        r = self.connection.execute(query_to_evaluate)

