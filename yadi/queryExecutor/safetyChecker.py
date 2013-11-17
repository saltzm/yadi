from ..dataStructures.query import *
from .exceptions import *

class SafetyChecker():
    def check_for_safety(self,query):
        if isinstance(query, ConjunctiveQuery):
            sq = ConjunctiveQuerySafetyChecker()
        if isinstance(query, DisjunctiveQuery):
            sq = DisjunctiveQuerySafetyChecker()
        return sq.check_for_safety(query)

class ConjunctiveQuerySafetyChecker():

    def check_for_safety(self,query):
        var_dict = query.get_var_dict()
        safe_variables = self.get_safe_variables(query,var_dict)
        return (self.check_head(safe_variables,query) and
               self.check_negated_goals(safe_variables,query) and
               self.check_non_equality_explicit_constraints(safe_variables,query))

    def check_head(self,safe_variables,query):

        for variable in list(query.head_relation.get_variables()):
            if not (variable in safe_variables):
                raise NotSafeException('Query not safe because '+ variable.name + ' occurs in the head and not in a positive goal')
                return False
        return True

    def check_negated_goals(self,safe_variables,query):

        # Create a list of variables which occur in negated goals.
        variables_in_negated_goals = [y for x in query.relations for y in list(x.variables) if x.is_negated()]

        # And check them:
        for variable in variables_in_negated_goals:
            if not (variable in safe_variables):
                raise NotSafeException('Query not safe because ' + variable.name + ' from a negated goal does not occur in a positive goal')
                return False

        return True


    def check_non_equality_explicit_constraints(self,safe_variables,query):

        # Checking variables which occur in explicit constraints with non equality operators

        # Create a list of variables which occur in explicit constraints with non equality operators
        variables_in_constraints_with_non_equality_operators = [y for x in query.constraints \
                                                                    for y in [x.get_left_side(),x.get_right_side()] \
                                                                        if y.is_variable() and not x.is_equality_constraint()]

        for variable in variables_in_constraints_with_non_equality_operators:
            if not (variable in safe_variables):
                raise NotSafeException('Query not safe because ' + variable.name + ' from a non_equality comparison does not occur in a positive goal')
                return False

        return True

    def get_safe_variables(self,query,var_dict):
        # Create a list of safe variables: variables bounded to constants or that occur in a positive goal

        variables_bounded_to_constants = []

        for constraint in query.constraints:
            if (constraint.get_left_side().is_variable() and
                constraint.get_right_side().is_constant() and
                constraint.is_equality_constraint()):
                    variables_bounded_to_constants.append(constraint.get_left_side())

        safe_variables = list(var_dict) + variables_bounded_to_constants

        return safe_variables


