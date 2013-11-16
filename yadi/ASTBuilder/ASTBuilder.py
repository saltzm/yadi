__author__ = 'caioseguin'

from dataStructures.constraint import Constraint
from dataStructures.element import Variable, Constant, Wildcard
from dataStructures.query import ConjunctiveQuery
from dataStructures.relation import RelationInQuery

# This class acts as the middle man between the Datalog parser and the SQL translator.
# It transforms the parser's output into a list of conjunctiveQueries and a list of disjunctiveQueries.

# Operators used in this module

ruleOperator = ':-'
disjunctionOperator = ';'
greaterOperator = '>'
lessOperator = '<'
greaterEqualOperator = '>='
lessEqualOperator = '<='
equalOperator = '='
negationOperator = 'not'
forbiddenSymbol = '$'


class ASTBuilder:
    # Each element of the list program_ast consists in a list. Each sub-list start with a conjunctiveQuery or a
    # disjunctiveQuery Object, followed by a number of relationInQuery Objects. A new sub-list is appended every time a
    # new line from the parsed datalog program is handled.
    # The program_ast is going to be passed along statement by statement.
    # The history_ast is the whole history of datalog programs handled by the ASTBuilder.

    # The RuleHandler is responsible of translating every rule into the ast form

    history_ast = []
    program_ast = []
    ruleHandler = None

    def __init__(self, script_input_flag):
        self.script_input_flag = script_input_flag
        history_ast = []
        program_ast = []
        ruleHandler = RuleHandler()


    def buildAST(self, parsed_datalog_program):

        assert isinstance(parsed_datalog_program, list)

        program_ast = []

        for code_line in parsed_datalog_program:
            self.program_ast.append(self.handleCodeLine(code_line))

        return program_ast

        self.history_ast.append(program_ast)

    def handleCodeLine(self, code_line):

        assert isinstance(code_line, list)

        code_line_ast = []

        for statement in code_line:
            statement_ast = self.handleStatement(statement)
            code_line_ast.append(statement_ast)

        return code_line_ast

    def handleStatement(self, statement):

        assert isinstance(statement, list)

        if self.script_input_flag:

            if self.ruleHandler.isRule(statement):
                statement_ast = self.handleRule(statement)
            else:
                raise Exception("?.handleFact(statement) not implemented yet")

        else:
            raise Exception("?.handleQuery(statement) not implemented yet")

        return statement_ast

    def handleRule(self, statement):

        assert isinstance(statement, list)

        if self.ruleHandler.isDisjunctiveRule(statement):
            raise Exception("self.ruleHandler.handleDisjunctiveRule(statement) not implemented yet")
        else:
            return self.ruleHandler.handleConjunctiveRule(statement)


class RuleHandler:
    def __init__(self):
        pass

    def handleConjunctiveRule(self, rule):

        assert isinstance(rule, list)

        if len(rule) != 1:
            raise Exception("list with exactly one element expected")
        else:
            rule = rule[0] # Peal list

        head = self.extractHead(rule)
        body = self.extractBody(rule)

        relation_object_list, constraint_object_list = self.handleBody(body)
        query_object = self.handleHead(head, relation_object_list, constraint_object_list)

        return query_object

    def handleHead(self, head, relation_object_list, constraint_object_list):
        head_relation = self.handleRelation(head)
        return ConjunctiveQuery(relation_object_list, constraint_object_list, head_relation)

    def handleBody(self, body):

        assert isinstance(body, list)

        relation_list = []
        constraint_list = []

        for body_part in body:
            if self.isConstraint(body_part):
                relation_list.extend(self.handleConstraint(body_part))
            else:
                constraint_list.extend(self.handleRelation(body_part))

        return relation_list, constraint_list

    def handleRelation(self, relation):

        assert isinstance(relation, list)

        if self.isNegatedRelation(relation):
            is_negated = True
            relation = relation[1:len(relation)][0]
        else:
            is_negated = False

        relation_symbol = relation[0]

        if not isinstance(relation[1], list):
            raise Exception("list of terms expected")
        else:
            term_list = relation[1]

        ast_term_list = self.handleTermList(term_list)
        new_relation_in_query = RelationInQuery(relation_symbol, ast_term_list, is_negated)
        return new_relation_in_query

    def handleTermList(self, term_list):

        ast_term_list = []

        for term in term_list:
            if term.isupper():
                ast_term_list.extend(Variable(term))
            if term.islower():
                ast_term_list.extend(Constant(term))
            if term == '_':
                ast_term_list.extend(Wildcard())

        return ast_term_list

    def handleConstraint(self, constraint):
        return Constraint(constraint[0], constraint[1], constraint[2])

    def extractHead(self, rule):
        return rule[0]

    def extractBody(self, rule):
        if not len(rule) >= 3:
            raise Exception("list with three or more elements expected for a body")
        return rule[2:len(rule)]

    def isRule(self, statement):
        return ruleOperator in statement[0]

    def isDisjunctiveRule(self, statement):
        return disjunctionOperator in statement[0]

    def isNegatedRelation(self, relation):
        return relation[0] == negationOperator

    def isConstraint(self, body_part):
        return (len(body_part) == 3) and ( ( body_part[1] == greaterOperator ) or
                                           ( body_part[1] == greaterEqualOperator ) or
                                           ( body_part[1] == lessOperator ) or
                                           ( body_part[1] == lessEqualOperator ) or
                                           ( body_part[1] == equalOperator ))