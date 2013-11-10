#TODO: 

# Check the IS EQUALITY or IS IS COMPARISON in check_is_it_safe() (there's 2 things to check).
# Implement check variables that occur in defined predicates.

class Element:
    pass

class Variable(Element):
    def __init__(self,name = ''):
        self.name = name

class Constant(Element):
    def __init__(self,value = ''):
        self.value = value

class RelationInQuery:

    def __init__(self, name='', variables={},constants = {},wildcards = [], is_negated = False):
        self.name = name # The name of the relation
        self.variables = variables # {Variable -> Position}
        self.constants = constants # {Constant -> Position}
        self.negated = False # Is it negated
        self.wildcards = wildcards # [position]  


class Query:
    def __init__(self, relations = [], constraints = [], head_variables = [] ):
        self.head_variables = head_variables
        self.relations = relations# [RelationInQuery].
        self.constraints = constraints # Explicit constraints of the form Element COMP Element type.
                                       # [(Element_1, Element_2, Comparison_operator)]

class QueryToAlchemyStatement:
    def __init__(self, query):
        self.query = query
        self.var_dict = {} # Variable -> [(Relation, field)]
        for relation in query.relations:
                    for var in relation.variables.keys():
                        if var_dict.has_key(var):
                            var_dict[var].append((relation.name,relation.variables[var]))
                        else:
                            var_dict[var] = [(relation.name,relation.variables[var])]

    def getJoinConstraints():
        constraints = []
        for var in self.var_dict.keys():
            length = len(self.var_dict[var])
            for i in range(0,length):
                (rel_i, pos_i) = self.var_dict[var][i]
                for j in range(i, length):
                    (rel_j, pos_j) = self.var_dict[var][j]
                    constraints.append(rel_i + '.' + pos_i + '=' + rel_j + '.' + pos_j) # Generate the corresponding join
        return constraints

    def getImplicitConstraints():
        constraints = []
        # An implicit constraint is one in which you have a constant inside a relation.
        for relation in self.query.relations:
            for (constant,position) in relation.constants:
                constraints.append(relation.name+'.'+position + '='+constant)
        return constraints

    def getExplicitConstraints():
        constraints = []
        # An explicit constraint is one of the form Element COMP Element type.
        for constraint in self.query.constraints:
            if instance(constraint[0],Variable):
                left_side = self.var_dict[constraint[0]][0]+'.'+self.var_dict[constraint[0]][1]
            else:
                left_side = constraint[0].value

            if instance(constraint[1],Variable):
                right_side = self.var_dict[constraint[1]][0]+'.'+self.var_dict[constraint[1]][1]
            else:
                right_side = constraint[1].value

            constraints.append(left_side + constraint[2] + right_side)
        return constraints

    def getSelectedColumns():
        pass # TODO

    def getNotExistsClauses():
        for relation in self.query.relations:
            if relation.negated:
                for variable in relation.variables:
                    pass

    
    def check_is_it_safe():

        # Create a list of safe variables: variables bounded to constants or that occur in a positive goal

        variables_bounded_to_constants = []

        for constraint in self.query.constraints:
            if ((instance(constraint[0],Variable) and instance(constraint[1],Constant)) or 
               (instance(constraint[0],Constant) and instance(constraint[1],Variable))): #and 
# CHECK THIS              (instance(constraint[2],Equality) or instance(constraint[2],Is)):

                if instance(constraint[0],Variable):
                    variables_bounded_to_constants.append(constraint[0])
                else:
                    variables_bounded_to_constants.append(constraint[1])

        safe_variables = self.var_dict.keys() + variables_bounded_to_constants

        # Checking head variables

        for variable in self.query.head_variables:
            if not (variable in safe_variables):
                return False

        # Checking variables in negated goals

        # Create a list of variables which occur in negated goals. 
        variables_in_negated_goals = []

        for negated_relation in self.query.relations:
            variables_in_negated_goals += negated_relation.variables.keys()

        # And check them:

        for variable in variables_in_negated_goals:
            if not (variable in safe_variables):
                return False

        # Checking variables which occur in defined predicates

# TODO

        # Checking variables which occur in explicit constraints with non equality operators

        # Create a list of variables which occur in explicit constraints with non equality operators
        variables_in_constraints_with_non_equality_operators = []

        for constraint in self.query.constraints:
            if instance(constraint[0],Variable): #and 
# CHECK THIS              not (instance(constraint[2],Equality) or instance(constraint[2],Is)):
                variables_in_constraints_with_non_equality_operators.append(constraint[0])
            if instance(constraint[1],Variable): #and 
# CHECK THIS              not (instance(constraint[2],Equality) or instance(constraint[2],Is)
                variables_in_constraints_with_non_equality_operators.append(constraint[1])
        # And check them:

        for variable in variables_in_constraints_with_non_equality_operators:
            if not (variable in safe_variables):
                return False

        return True

    def generateAlchemyStatement(query):

        check_is_it_safe()

        select_clause = 'SELECT ' + ','.join(getSelectedColumns())
        from_clause = 'FROM bla'
        where_clause = 'WHERE ' + ','.join(getExplicitConstraints(), getImplicitConstraints(), getJoinConstraints())

        return select_clause + from_clause + where_clause
