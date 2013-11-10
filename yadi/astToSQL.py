#TODO: 

# Check the IS EQUALITY or IS IS COMPARISON in check_is_it_safe() (there's 2 things to check).
# Implement check variables that occur in defined predicates.

class Element:
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)

class Variable(Element):
    def __init__(self,name = ''):
        self.name = name
    def __hash__(self):
        return hash(self.name)
    def __repr__(self):
        return self.name

class Constant(Element):
    def __init__(self,value = ''):
        self.value = value
    def __hash__(self):
        return hash(self.value)
    def __repr__(self):
        return self.name

class RelationInQuery:

    def __init__(self, name='', variables={},constants = {},wildcards = [], is_negated = False):
        self.name = name # The name of the relation
        self.variables = variables # {Variable -> Position}
        self.constants = constants # {Constant -> Position}
        self.is_negated = is_negated # Is it negated
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

        variables_in_positive_goals = [y for x in self.query.relations for y in x.variables.keys() if not x.is_negated] 

        for relation in [x for x in self.query.relations if not x.is_negated]:
            for var in relation.variables.keys():
                if self.var_dict.has_key(var):
                    self.var_dict[var].append((relation.name,relation.variables[var]))
                else:
                    self.var_dict[var] = [(relation.name,relation.variables[var])]

    def getJoinConstraints(self):
        constraints = []
        for var in self.var_dict.keys():
            length = len(self.var_dict[var])
            for i in range(0,length):
                (rel_i, pos_i) = self.var_dict[var][i]
                for j in range(i, length):
                    (rel_j, pos_j) = self.var_dict[var][j]
                    constraints.append(rel_i + '.' + pos_i + '=' + rel_j + '.' + pos_j) # Generate the corresponding join
        return constraints

    def getImplicitConstraints(self):
        constraints = []
        # An implicit constraint is one in which you have a constant inside a relation.
        for relation in self.query.relations:
            for (constant,position) in relation.constants:
                constraints.append(relation.name+'.'+position + '='+constant)
        return constraints

    def getExplicitConstraints(self):
        constraints = []
        # An explicit constraint is one of the form Element COMP Element type.
        for constraint in self.query.constraints:
            if isinstance(constraint[0],Variable):
                left_side = self.var_dict[constraint[0]][0]+'.'+self.var_dict[constraint[0]][1]
            else:
                left_side = constraint[0].value

            if isinstance(constraint[1],Variable):
                right_side = self.var_dict[constraint[1]][0]+'.'+self.var_dict[constraint[1]][1]
            else:
                right_side = constraint[1].value

            constraints.append(left_side + constraint[2] + right_side)
        return constraints

    def getSelectedColumns(self):
        pass # TODO

    def getNotExistsClauses(self):
        for relation in self.query.relations:
            if relation.negated:
                for variable in relation.variables:
                    pass

    
    def check_is_it_safe(self):
        
        # Create a list of safe variables: variables bounded to constants or that occur in a positive goal

        variables_bounded_to_constants = []

        for constraint in self.query.constraints:
            if ((isinstance(constraint[0],Variable) and isinstance(constraint[1],Constant)) or 
               (isinstance(constraint[0],Constant) and isinstance(constraint[1],Variable))) and constraint[2] == '=': #and 
# CHECK THIS              (isinstance(constraint[2],Equality) or isinstance(constraint[2],Is)):

                if isinstance(constraint[0],Variable):
                    variables_bounded_to_constants.append(constraint[0])
                else:
                    variables_bounded_to_constants.append(constraint[1])

        safe_variables = self.var_dict.keys() + variables_bounded_to_constants

        return (self.check_head(safe_variables) and 
               self.check_negated_goals(safe_variables) and 
               self.check_defined_predicates (safe_variables) and 
               self.check_non_equality_explicit_constraints(safe_variables))

    def check_head(self,safe_variables):

        for variable in self.query.head_variables:
            if not (variable in safe_variables):
                print 'Failing because '+ variable.name + ' occurs in the head and not in a positive goal'
                return False
        return True

    def check_negated_goals(self,safe_variables):

        # Create a list of variables which occur in negated goals. 
        variables_in_negated_goals = [y for x in self.query.relations for y in x.variables.keys() if x.is_negated] 

        # And check them:
        for variable in variables_in_negated_goals:
            if not (variable in safe_variables):
                print 'Not safe because ' + variable.name + ' from a negated goal does not occur in a positive goal'
                return False

        return True

    def check_defined_predicates(self,safe_variables):
        # Checking variables which occur in defined predicates
# TODO
        return True

    def check_non_equality_explicit_constraints(self,safe_variables):

        # Checking variables which occur in explicit constraints with non equality operators

        # Create a list of variables which occur in explicit constraints with non equality operators
        variables_in_constraints_with_non_equality_operators = []

        for constraint in self.query.constraints:
            if isinstance(constraint[0],Variable) and constraint[2] == '=': #and 
# CHECK THIS              not (isinstance(constraint[2],Equality) or isinstance(constraint[2],Is)):
                variables_in_constraints_with_non_equality_operators.append(constraint[0])
            if isinstance(constraint[1],Variable) and constraint[2] == '=': #and 
# CHECK THIS              not (isinstance(constraint[2],Equality) or isinstance(constraint[2],Is)
                variables_in_constraints_with_non_equality_operators.append(constraint[1])
        # And check them:

        for variable in variables_in_constraints_with_non_equality_operators:
            if not (variable in safe_variables):
                return False

        return True

    def generateAlchemyStatement(self,query):

        check_is_it_safe()

        select_clause = 'SELECT ' + ','.join(getSelectedColumns())
        from_clause = 'FROM bla'
        where_clause = 'WHERE ' + ','.join(getExplicitConstraints(), getImplicitConstraints(), getJoinConstraints())

        return select_clause + from_clause + where_clause
