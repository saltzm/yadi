from .TranslationWrapper.translateDatalogToSQL import translateDatalogToSql
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
    print("/dbschema - Lists the database schema.\n")
    print("/help - Prints a list of available commands with their descriptions.\n")
    print("/script \"path\" - Loads a Datalog program from a file in the specified path."
          " Usage example: /script \"C:/file.txt\" \n")
    print("/quit - Quits YADI.\n")
    print("====================")


def quit_yadi():
    sys.exit(0)


def clrscr():
    os.system('cls' if os.name == 'nt' else 'clear')

def do_assert():
    pass


def loadscript(path):
    np = path.replace('\"', '')
    print("Loading file from: "+np)
    str_concat = ""

    try:
        with open(np, 'r') as f:
            for data_line in f:
                str_concat += data_line
            print("Datalog program read:\n"+SyntaxHighlight().highlight(str_concat)+"\n")
            execute_translation(str_concat)
    except Exception as e:
        print(Fore.RED+str(e)+Fore.RESET)


def execute_translation(input_line):
    sql_queries = translateDatalogToSql(input_line)
    print(sql_queries)
    for s in sql_queries:
        try:
            evaluateQuery().evaluate(s)
        except Exception as e:
            print(e)


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

To begin, type a Datalog query. For a list of commands, type /help
"""
    print(Fore.YELLOW+introString+Fore.RESET)

    while True:
        print("")
        read_line = input('yadi> ').strip()

        if read_line == "":
            print(Fore.RED+"Interpreter error: Empty is not a valid input."+Fore.RESET)
            continue

        int_parser = IntParse()

        if read_line[0] == "/":
            try:
                parsed_statement = int_parser.parse_command(read_line)

                if parsed_statement[0] == "/quit":
                    quit_yadi()
                elif parsed_statement[0] == "/help":
                    help()
                elif parsed_statement[0] == "/assert":
                    do_assert()
                elif parsed_statement[0] == "/script ":
                    loadscript(parsed_statement[1])
                elif parsed_statement[0] == "/clrscr":
                    clrscr()

            except InterpreterException as e:
                print(Fore.RED+"Interpreter error: "+str(e)+Fore.RESET)
        else:
            execute_translation(read_line)

init()
start()
