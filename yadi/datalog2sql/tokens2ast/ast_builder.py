__author__ = 'caioseguin'

from .rule_handler import RuleHandler
from ..query_data_structures.query import *

# This class acts as the middle man between the Datalog parser and the SQL translator.
# It transforms the parser's output into a list of conjunctiveQueries and a list of disjunctiveQueries.

class ASTBuilder:
    # Each element of the list program_ast consists in a list. Each sub-list start with a conjunctiveQuery or a
    # disjunctiveQuery Object, followed by a number of relationInQuery Objects. A new sub-list is appended every time a
    # new line from the parsed datalog program is handled.
    # The program_ast is going to be passed along statement by statement.
    # The history_ast is the whole history of datalog programs handled by the ASTFactory.

    # The RuleHandler is responsible of translating every rule into the ast form

    history_ast = []
    program_ast = []
    rule_handler = RuleHandler()

    def __init__(self):
        history_ast = []
        program_ast = []
        rule_handler = RuleHandler()


    def buildAST(self, parsed_datalog_program, is_assertion):

        assert isinstance(parsed_datalog_program, list)

        self.program_ast = []

        for code_line in parsed_datalog_program:
            x = self.handleStatement(code_line, is_assertion)
            self.program_ast.append(x)

        self.history_ast.append(self.program_ast)

        return self.program_ast

    def handleStatement(self, statement, is_assertion):

        assert isinstance(statement, list)

        if is_assertion:
            if self.rule_handler.isRule(statement):
                statement_ast = AssertedQuery(self.handleRule(statement))
            else:
                statement_ast = AssertedQuery(self.handleFact(statement), True)
        else:
            if self.rule_handler.isRule(statement):
                statement_ast = self.handleRule(statement)
            else:
                statement_ast = self.handleFact(statement)

        return statement_ast

    def handleRule(self, statement):

        assert isinstance(statement, list)

        if self.rule_handler.isDisjunctiveRule(statement):
            return self.rule_handler.handleDisjunctiveRule(statement)
        else:
            return self.rule_handler.handleConjunctiveRule(statement)

    def handleFact(self, statement):
        assert isinstance(statement, list)
        return self.rule_handler.handleFact(statement)
