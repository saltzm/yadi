__author__ = 'caioseguin'


from ..dataStructures.constraint import Constraint
from ..dataStructures.element import Variable, Constant, Wildcard
from ..dataStructures.query import ConjunctiveQuery
from ..dataStructures.relation import RelationInQuery

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

class RuleHandler:
    def __init__(self):
        pass

    def handleFact(self, fact):
        relation_object_list, constraint_object_list = self.handleBody(fact)
        return ConjunctiveQuery(relation_object_list, constraint_object_list, None)

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

        if self.isNegatedRelation(relation):
            is_negated = True
            relation = relation[1:len(relation)][0]
        else:
            is_negated = False

        relation_symbol = relation[0]
        # TODO
#        if len(relation) == 1:
#            raise Exception("Atoms not yet supported")

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

    def isRule(self, statement):
        return ruleOperator in statement

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

    def isVariable(self, term):
        return term.isupper()

    def isConstant(self, term):
        return term.islower() or term.isdigit() or (term[0] == "'" and term[len(term)-1] == "'")

    def isWildcard(self, term):
        return term == '_'

    def handleConstant(self, constant):
        if constant[0] == "'" and constant[len(constant)-1] == "":
            return constant[1:len(constant)-1]
        else:
            return constant
