__author__ = 'caioseguin'

from ..query_data_structures.constraint import Constraint
from ..query_data_structures.element import Variable, Constant, Wildcard
from ..query_data_structures.query import *
from ..query_data_structures.relation import RelationInQuery

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
assertCommand = '/assert '

class RuleHandler:
    def __init__(self):
        pass

    def handleFact(self, fact):
        relation_object_list, constraint_object_list = self.handleBody(fact)
        return ConjunctiveQuery(relation_object_list, constraint_object_list, None)

    def handleDisjunctiveRule(self, rule):

        assert isinstance(rule, list)

        query_object_list = []
        head = self.extractHead(rule)
        body = self.extractBody(rule)

        conjunctive_body_list = self.splitDisjunctiveRule(body)

        for conjunctive_body in conjunctive_body_list:
            conjunctive_rule = []
            conjunctive_rule.append(head)
            conjunctive_rule.append(ruleOperator)
            conjunctive_rule.append(conjunctive_body)

            query_object_list.append(self.handleConjunctiveRule(conjunctive_rule))

        return DisjunctiveQuery(query_object_list)


    def handleConjunctiveRule(self, rule):

        assert isinstance(rule, list)

        #if len(rule) != 1:
        #    raise Exception("list with exactly one element expected")
        #else:
        #    rule = rule[0] # Peal list
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
                constraint_list.append(self.handleConstraint(body_part))
            else:
                relation_list.append(self.handleRelation(body_part))

        return relation_list, constraint_list

    def handleRelation(self, relation):

        assert isinstance(relation, list)

        if len(relation) == 1:
            raise Exception("Atoms not supported")

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


    # Will have to be updated to deal with strings as constants
    def handleTermList(self, term_list):

        ast_term_list = []

        for term in term_list:
            if self.isVariable(term):
                ast_term_list.append(Variable(term))
            if self.isConstant(term):
                ast_term_list.append(Constant(self.handleConstant(term)))
            if self.isWildcard(term):
                ast_term_list.append(Wildcard())

        return ast_term_list

    # Will have to be updated to deal with strings as constants
    def handleConstraint(self, constraint):

        if self.isVariable(constraint[0]):
            left_side = Variable(constraint[0])
        else:
            left_side = Constant(self.handleConstant(constraint[0]))

        if self.isVariable(constraint[2]):
            right_side = Variable(constraint[2])
        else:
            right_side = Constant(self.handleConstant(constraint[2]))

        return Constraint(left_side, right_side, constraint[1])

    def extractHead(self, rule):
        return rule[0]

    def extractBody(self, rule):
        if not len(rule) >= 3:
            raise Exception("list with three or more elements expected for a body")
        return rule[2:len(rule)]

    def splitDisjunctiveRule(self, disjunctive_query):

        conjunctive_query_list = []
        conjunctive_query = []

        for element in disjunctive_query:


            if element == disjunctionOperator:
                conjunctive_query_list.append(conjunctive_query)
                conjunctive_query = []
            else:
                conjunctive_query.extend(element)

        conjunctive_query_list.append(conjunctive_query)

        return conjunctive_query_list


    def isRule(self, statement):
        return ruleOperator in statement

    def isDisjunctiveRule(self, statement):
        return disjunctionOperator in statement

    def isAssertion(self, statement):
        return statement[0] == assertCommand

    def isNegatedRelation(self, relation):
        return relation[0] == negationOperator

    def isConstraint(self, body_part):
        return (len(body_part) == 3) and ( ( body_part[1] == greaterOperator ) or
                                           ( body_part[1] == greaterEqualOperator ) or
                                           ( body_part[1] == lessOperator ) or
                                           ( body_part[1] == lessEqualOperator ) or
                                           ( body_part[1] == equalOperator ))

    def isVariable(self, term):
        return term[0].isupper()

    def isConstant(self, term):
        return term[0].islower() or term.isdigit() or (term[0] == "'" and term[len(term)-1] == "'")

    def isWildcard(self, term):
        return term == '_'

    def handleConstant(self, constant):
        if constant[0] == "'" and constant[len(constant)-1] == "":
            return constant[1:len(constant)-1]
        else:
            return constant
