import cmd, sys
from yadi import *
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from tabulate import tabulate
from ..TranslationWrapper import translateDatalogToSQL


class Interpreter(cmd.Cmd):
    intro = '\nWelcome to the YADI project.\nType help or ? to list commands.\n'
    prompt = 'YADI> '
    engine = None
    db = ""
    user = ""
    host = ""
    port  = ""

    def emptyline(self):
        return

    def parseline(self, line):
        """Parse the line into a command name and a string containing
        the arguments.  Returns a tuple containing (command, args, line).
        'command' and 'args' may be None if the line couldn't be parsed.
        """

        line = line.strip()
        if not line:
            return None, None, line
        elif line[0] == '?':
            line = 'help ' + line[1:]
            return super().parseline(line)
        elif line[0] == '/':
            return super().parseline(line[1:])
        else:
            return None, None, line

        #--commands--
    def do_open_db(self, arg):
        'Open database connection with the supplied arguments:\n\nopen_db username password database host=localhost port=5432\n'
        args = arg.split()
        args_len = len(args)

        if (args_len < 3):
            print("YADI was not able to create a database connection")
            super().do_help("open_db")
            return

        username = args[0]
        password = args[1]
        database = args[2]
        host = None
        port = None

        if(args_len >= 4):
            host  = args[3]

        if(args_len == 5):
            port = args[4]

        connection_string = URL('postgresql', username, password, host, port, database)
        new_engine = create_engine(connection_string, echo=False)

        if(new_engine):
            self.engine = new_engine
            try:
                connection = self.engine.connect()
                connection.close()
                self.user = username
                self.db = database = args[2]
                if(host):
                    self.host = host
                else:
                    self.host = "localhost"
                if(port):
                    self.port = port
                else:
                    self.port = "5432"
                print("YADI is connected to database: "+ database)
            except Exception as e:
                print("Error creating connection to database:\n{0}".format(e.args[0]))
                return
        else:
            print("YADI was not able to create a database connection")
            super().do_help("open_db")
            return

    def do_consult(self, line):
        "Loads facts or rules from a file on absolute filePath"
        return

    def do_consult_queries(self, line):
        "Load queries from a file on absolute filePath"
        return

    def do_assertion(self, line):
        "Creates a fact or a rule"
        return

    def do_current_db(self, line):
        "Information about the current database"
        if(not(self.engine)):
            print("Not connected to any database.")
        else:
            print("Current database: " + self.db+"     User: " + self.user +"\nHost: " + self.host+"     Port: " + self.port)
        return

    def do_quit(self, arg):
        'Close the YADI window, and exit'
        print('Thank you for using YADI')
        self.close()
        return True

    def default(self, line):

        if(not(self.engine)):
            print("YADI is not connected to a database. Please use /open_db command")
            super().do_help("open_db")
            return

        try:
            datalog_statement = self.preprocess(line)
            sql = translateDatalogToSql(datalog_statement)

            connection = self.engine.connect()

            for query in sql:
                print(query + '\n')
                result = connection.execute(query)
                print(tabulate(result))

            connection.close()

        except Exception as e:
            print("Error querying the database:")
            print(e)
            return

    def preprocess(self, line):
        #line = line.lower()
        #if self.file and 'playback' not in line:
        #    print(line, file=self.file)
        return line

    def close(self):

        if self.engine:
            self.engine.dispose()
            self.engine= None
