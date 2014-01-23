from .datalog2sql.datalog2sqlconverter import Datalog2SqlConverter
from .evaluate_query import *
from colorama import *
from .interpreter.interpreterParse import *
from .interpreter.syntaxHighlighter import SyntaxHighlight
import sys
import os


def help():
    print("========HELP========")
    print("\nThe following commands are supported by YADI:")
    print("/assert - Used to interactively add new rules to the database. Usage example: /assert a(a4)\n")
    print("/clrscr - Clears the terminal.\n")
    print("/curdb - Shows the current database path.\n")
    print("/dbschema - Lists the database schema.\n")
    print("/help - Prints a list of available commands with their descriptions.\n")
    print("/script \"path\" - Loads a Datalog program from a file in the specified path."
          " Usage example: /script \"C:/file.txt\" \n")
    print("/setdb - Set the database to use with YADI. The last configuration before quitting YADI will persist"
          " for the next session.\n")
    print("/quit - Quits YADI.\n")
    print("====================")


def dbschema():
    pass


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
    evaluateQuery().set_engine(str_engine)


def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')


def do_assert(statement):
    print("Do the assert here for "+statement)
    pass


def loadscript(path):
    np = path.replace('\"', '')
    print("Loading file from: "+np)
    str_concat = ""

    try:
        with open(np, 'r') as f:
            for data_line in f:
                str_concat += data_line
            print("Datalog program read:\n"+SyntaxHighlight().highlight(str_concat))
            execute_translation(str_concat)
    except Exception as e:
        print(Fore.RED+str(e)+Fore.RESET)


def execute_translation(input_line):
    sql_queries = Datalog2SqlConverter().convertDatalog2Sql(input_line)
    for s in sql_queries:
        try:
            evaluateQuery().evaluate(s)
        except Exception as e:
            print(Fore.RED+'Query evaluation error: '+str(e)+Fore.RESET)


def get_db_url():
    print(Fore.YELLOW+"Current configuration:")
    evaluateQuery().print_engine_url()
    print(Fore.RESET)


def quit_yadi():
    evaluateQuery().dispose_last()
    evaluateQuery().saveconf()
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
    if evaluateQuery().initialize_db():
        get_db_url()

    while True:
        print(Fore.YELLOW+'\nyadi> '+Fore.RESET, end="")
        read_line = input().strip()

        if read_line == "":
            print(Fore.RED+"Interpreter error: Empty is not a valid input. For help, type /help"+Fore.RESET)
            continue

        int_parser = IntParse()

        if read_line[0] == "/":
            try:
                parsed_statement = int_parser.parse_command(read_line)

                if parsed_statement[0] == "/quit":
                    quit_yadi()
                elif parsed_statement[0] == "/help":
                    help()
                elif parsed_statement[0] == "/assert ":
                    do_assert(parsed_statement[1])
                elif parsed_statement[0] == "/script ":
                    loadscript(parsed_statement[1])
                elif parsed_statement[0] == "/clrscr":
                    clrscr()
                elif parsed_statement[0] == "/setdb":
                    set_db()
                elif parsed_statement[0] == "/curdb":
                    get_db_url()
            except InterpreterException as e:
                print(Fore.RED+"Interpreter error: "+str(e)+Fore.RESET)
        else:
            execute_translation(read_line)

init()
start()
