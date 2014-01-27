from .datalog2sql.datalog2sqlconverter import Datalog2SqlConverter
from .sql_engine.query_evaluator import QueryEvaluator
from .sql_engine.db_state_tracker import DBStateTracker
from colorama import *
from .interpreter.interpreter_parse import *
from .interpreter.syntax_highlighter import SyntaxHighlight
import sys
import os

qe = QueryEvaluator()
db_state_tracker = DBStateTracker(qe)
converter = Datalog2SqlConverter(db_state_tracker)

def help():
    print("========HELP========")
    print("\nThe following commands are supported by YADI:")
    print("/assert - Used to interactively add new rules to the database. Usage example: /assert a(a4)\n")
    print("/clrscr - Clears the terminal.\n")
    print("/curdb - Shows the current database path.\n")
    print("/dbschema - Lists the database schema.\n")
    print("/dropview <view name> - Drops the view from the database.\n")
    print("/droptable <table name> - Drops the table from the database. \
            (WARNING: Drop cascades to dependent views.)\n")
    print("/help - Prints a list of available commands with their descriptions.\n")
    print("/script \"path\" - Loads a Datalog program from a file in the specified path."
          " Usage example: /script \"C:/file.txt\" \n")
    print("/setdb - Set the database to use with YADI. The last configuration before quitting YADI will persist"
          " for the next session.\n")
    print("/quit - Quits YADI.\n")
    print("====================")


def dbschema():
    qe.get_schema()


def set_db():
    print("Setting database parameters. To quit at any time, type /quitset")
    args = [[], []]

    args[0].append("Username> ")
    args[0].append("Password> ")
    args[0].append("Host> ")
    args[0].append("Port> ")
    args[0].append("Database> ")

    for i in range(0, 5):
        x = ""

        while x == "":
            print(Fore.YELLOW+args[0][i]+Fore.RESET, end="")
            x = input().strip()
            if x == "" and i is not 1:
                print(Fore.RED+"Error: Field cannot be left blank."+Fore.RESET)
            if i is 1 and x == "":
                break

        if x == "/quitset":
            return
        args[1].append(x)

    str_engine = 'postgresql://'+args[1][0]
    if args[1][1] is not "":
        str_engine += ':' + args[1][1]

    str_engine += '@' + args[1][2] + ':' + args[1][3] + '/' + args[1][4]
    qe.set_engine(str_engine)


def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


def do_assert(input_line):
    line_to_trans = input_line[len('/assert'):]
    execute_translation(line_to_trans, True)


def loadscript(path):
    np = path.replace('\"', '')
    print("Loading file from: "+np)
    str_concat = ""

    try:
        with open(np, 'r') as f:
            for data_line in f:
                if not data_line.startswith('%'):
                    interpret_line(data_line)
                str_concat += data_line
            print("Datalog program read:\n"+SyntaxHighlight().highlight(str_concat))
    except Exception as e:
        print(Fore.RED+str(e)+Fore.RESET)


def execute_translation(input_line, is_assertion = False):
    sql_queries = converter.convertDatalog2Sql(
                    input_line,
                    is_assertion
                  )
    for s in sql_queries:
        try:
            qe.evaluate(s)
        except Exception as e:
            if not 'not return rows' in str(e):
                print(Fore.RED+'Query evaluation error: '+str(e)+Fore.RESET)


def get_db_url():
    print(Fore.YELLOW+"Current configuration:")
    qe.print_engine_url()
    print(Fore.RESET)

def drop_view(relation_name):
    try:
        qe.execute('DROP VIEW IF EXISTS ' + relation_name + ';')
    except Exception as e:
        print(Fore.RED+'Query evaluation error: '+str(e)+Fore.RESET)

def drop_relation(relation_name):
    try:
        qe.execute('DROP TABLE IF EXISTS ' + relation_name + ' CASCADE;')
    except Exception as e:
        print(Fore.RED+'Query evaluation error: '+str(e)+Fore.RESET)

# TODO: ensure called on ctrl-C
def quit_yadi():
    qe.dispose_last()
    qe.saveconf()
#    del db_state_tracker
    sys.exit(0)


def start():
    introString = """\
=========================================
                Welcome to
 __    __  ______   ____     ______
/\ \  /\ \/\  _  \ /\  _`\  /\__  _\\
\ `\`\\\\/'/\ \ \_\ \\\\ \ \/\ \\/_/\ \/
 `\ `\ /'  \ \  __ \\\\ \ \ \ \  \ \ \\
   `\ \ \   \ \ \/\ \\\\ \ \_\ \  \_\ \__
     \ \_\   \ \_\ \_\\\\ \____/  /\_____\\
      \/_/    \/_/\/_/ \/___/   \/_____/

   Yet Another Datalog Intepreter v1.0
=========================================

To begin, type a Datalog query. For a list of commands, type /help"""
    print(Fore.YELLOW+introString+Fore.RESET)
    if qe.initialize_db():
        get_db_url()

    while True:
        print(Fore.YELLOW+'\nyadi> '+Fore.RESET, end="")
        read_line = input().strip()
        interpret_line(read_line)

def interpret_line(read_line):
    read_line = read_line.strip()
    if read_line == "":
        return

    int_parser = IntParse()

    if read_line[0] == "/":
        try:
            parsed_statement = int_parser.parse_command(read_line)

            if parsed_statement[0] == "/quit":
                quit_yadi()
            elif parsed_statement[0] == "/help":
                help()
            elif parsed_statement[0] == "/assert ":
                do_assert(read_line)
            elif parsed_statement[0] == "/script ":
                loadscript(parsed_statement[1])
            elif parsed_statement[0] == "/clrscr":
                clrscr()
            elif parsed_statement[0] == "/setdb":
                set_db()
            elif parsed_statement[0] == "/curdb":
                get_db_url()
            elif parsed_statement[0] == "/dbschema":
                dbschema()
            elif parsed_statement[0] == "/dropview":
                drop_view(parsed_statement[1])
            elif parsed_statement[0] == "/droptable":
                drop_relation(parsed_statement[1])

        except InterpreterException as e:
            print(Fore.RED+"Interpreter error: "+str(e)+Fore.RESET)
    else:
        execute_translation(read_line)

init()
start()
