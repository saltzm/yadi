#TODO: 

# Check the IS EQUALITY or IS IS COMPARISON in check_is_it_safe() (there's 2 things to check).
# Implement check variables that occur in defined predicates.

import copy

equality_operator = '='

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
        return self.value

class RelationInQuery:

    def __init__(self, name='', variables={},constants = {},wildcards = [], is_negated = False):
        self.name = name # The name of the relation
        self.variables = variables # {Variable -> [Position]}
        self.constants = constants # {Constant -> [Position]}
        self.is_negated = is_negated # Is it negated
        self.wildcards = wildcards # [position]
    def __repr__(self):
        return ('name: ' + self.name + '\n' + 
               'variables: ' + str(self.variables) + '\n' +
               'constants: ' + str(self.constants) + '\n' + 
               'is_negated: ' + str(self.is_negated) + '\n' +
               'wildcards: ' + str(self.wildcards) + '\n')

class Query:
    def __init__(self, relations = [], constraints = [], head_variables = [] ):
        self.head_variables = head_variables
        self.relations = relations# [RelationInQuery].
        self.constraints = constraints # Explicit constraints of the form Element COMP Element type.
                                       # [[Variable, Element_2, Comparison_operator]]
                                       # Where Element_2 can be of the type Variable or Constant
    def __repr__(self):
        return ('Head vars: ' + str(self.head_variables) + '\n'+ 'Relations: ' + str(self.relations) + '\n' + 'Constraints: '+ str(self.constraints))# )
        
class QueryToAlchemyStatement:
    def __init__(self, query):
        self.query = copy.deepcopy(query)
        self.var_dict = self.create_var_dict(query) # Variable -> [(Relation, field)]

    # var_dict is a Variable -> [(Relation, field)] which is usefuld for several purposes.
    # It does not map occurences of variables in negated goals.
    def create_var_dict(self,query):
        variables_in_positive_goals = [y for x in query.relations for y in x.variables.keys() if not x.is_negated] 
        
        var_dict = {}

        for relation in [x for x in query.relations if not x.is_negated]:
            for var in relation.variables.keys():
                if not var_dict.has_key(var):
                    var_dict[var] = []
                for position in relation.variables[var]:
                    var_dict[var].append((relation,position))

        return var_dict

    def getJoinConstraints(self):
        constraints = []
        for var in self.var_dict.keys():
            length = len(self.var_dict[var])
            for i in range(0,length):
                (rel_i, pos_i) = self.var_dict[var][i]
                for j in range(i, length):
                    (rel_j, pos_j) = self.var_dict[var][j]
                    constraints.append(rel_i.name + '.' + pos_i + '=' + rel_j.name + '.' + pos_j) # Generate the corresponding join
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
                left_side = self.var_dict[constraint[0]][0].name+'.'+self.var_dict[constraint[0]][1]
            else:
                left_side = constraint[0].value

            if isinstance(constraint[1],Variable):
                right_side = self.var_dict[constraint[1]][0].name+'.'+self.var_dict[constraint[1]][1]
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

    def get_safe_variables(self):
        # Create a list of safe variables: variables bounded to constants or that occur in a positive goal

        variables_bounded_to_constants = []

        for constraint in self.query.constraints:
            if ((isinstance(constraint[0],Variable) and isinstance(constraint[1],Constant)) or 
               (isinstance(constraint[0],Constant) and isinstance(constraint[1],Variable))) and constraint[2] == equality_operator: #and 
# CHECK THIS              (isinstance(constraint[2],Equality) or isinstance(constraint[2],Is)):

                if isinstance(constraint[0],Variable):
                    variables_bounded_to_constants.append(constraint[0])
                else:
                    variables_bounded_to_constants.append(constraint[1])

        safe_variables = self.var_dict.keys() + variables_bounded_to_constants
        return safe_variables

    def check_is_it_safe(self):
        safe_variables = self.get_safe_variables()

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

# TODO clean this method:
    def check_non_equality_explicit_constraints(self,safe_variables):

        # Checking variables which occur in explicit constraints with non equality operators

        # Create a list of variables which occur in explicit constraints with non equality operators
        variables_in_constraints_with_non_equality_operators = []

        for constraint in self.query.constraints:
            if isinstance(constraint[0],Variable) and constraint[2] != equality_operator: #and 
# CHECK THIS              not (isinstance(constraint[2],Equality) or isinstance(constraint[2],Is)):
                variables_in_constraints_with_non_equality_operators.append(constraint[0])
            if isinstance(constraint[1],Variable) and constraint[2] != equality_operator: #and 
# CHECK THIS              not (isinstance(constraint[2],Equality) or isinstance(constraint[2],Is)
                variables_in_constraints_with_non_equality_operators.append(constraint[1])
        # And check them:
        print variables_in_constraints_with_non_equality_operators
        print safe_variables
        for variable in variables_in_constraints_with_non_equality_operators:
            if not (variable in safe_variables):
                return False

        return True

    ''' This method takes a query, makes a deep copy of it and modifies it to keep only equality constraints of the form:
        Var = const if Var occurs in the head OR
        const = const
        ie, constraints of the form Var1 = Var2, const = Var, Var = Const (if Var does not occur in the head) are eliminated.

        This makes several steps easier later on. 
        For instance, when checking if a variable is safe.
        
        In the following query Y should be safe. 

            R(X) := not T(Y), X = Y, X = 2

        And in the following query X should be safe

            R(X) := not T(Y), X = Y, S(Y)

        The only way to decide so is by noticing that because X=Y and X=2, Y must also be 2.
        This can be done if the equalities are reduced according to what was said previously:
        
            R(X) := not T(Y), X = Y, X = 2 is equivalent to:
            R(X) := not T(X), X = 2 is equivalent to:
            R(Y) := not T(Y), Y = 2 is equivalent to:

            
    '''  
    def reduce_equality_constraints(self,q):
        query = copy.deepcopy(q) 
        changed = True
        while changed:
            changed = False
            equality_constraints = [x for x in query.constraints if x[2] == equality_operator]
            for constraint in equality_constraints:
                # If it's an equality constraint of the form Const = Var, swap them unless the variable occurs in the head. Doing this simplifies the cases below:
                if isinstance(constraint[0],Constant) and isinstance(constraint[1],Variable):
                    changed = True
                    const = constraint[0]
                    var = constraint[1]

                    # Swap the variable and the constant. 
                    temp = var
                    constraint[1] = constraint[0]
                    constraint[0] = var

                # If it's an equality constraint of the form Var1 = Var2, substitute every occurence of Var1 with Var2
                # Occurences must be substituted in the head, in the list of variables and in the constraints
                if isinstance(constraint[0],Variable) and isinstance(constraint[1],Variable):
                    changed = True
                    var1 = constraint[0]
                    var2 = constraint[1]
                    # Replace every occurence of var1 in the head with var2.
                    for i in range(0,len(query.head_variables)):
                        if query.head_variables[i] == var1:
                            query.head_variables[i] = var2

                    # Replace every occurence of var1 in every relation with var2.
                        for relation in query.relations:
                            if relation.variables.has_key(var1):
                                occurences_of_the_variable = relation.variables[var1]
                                if relation.variables.has_key(var2):
                                    relation.variables[var2] += occurences_of_the_variable
                                else:
                                    relation.variables[var2] = occurences_of_the_variable
                                del relation.variables[var1]

                    # Replace every occurence of var1 in every constraint with var2
                        for query_constraint in query.constraints:
                            for query_constraint in query.constraints:
                                if query_constraint[0] == var1:
                                    query_constraint[0] = var2

                                if query_constraint[1] == var1:
                                    query_constraint[1] = var2 

                # If it's an equality constraint of the form Var = Const, replace the variable with the constant unless the variable occurs in the head.
                if isinstance(constraint[0],Variable) and isinstance(constraint[1],Constant):
                    var = constraint[0]
                    const = constraint[1] 
                    # Check if it occurs in the head
                    if not (var in query.head_variables):
                        changed = True
                        # Replace every occurence of this variable in every relation with the constant.
                        for relation in query.relations:
                            if relation.variables.has_key(var):
                                occurences_of_the_variable = relation.variables[var]
                                if relation.constants.has_key(const):
                                    relation.constants[const] += occurences_of_the_variable
                                else:
                                    relation.constants[const] = occurences_of_the_variable
                                del relation.variables[var]

                        # Replace every occurence of this variable in every constraint with the constant.
                        for query_constraint in query.constraints:
                            if query_constraint[0] == var:
                                query_constraint[0] = const

                            if query_constraint[1] == var:
                                query_constraint[1] = const 

                # Clean constraints of the form Element1 = Element1

                query.constraints =  [x for x in query.constraints if not x[0] == x[1]]

        return query                         

    def generateAlchemyStatement(self):

        # We modify the query object by removing unnecesary equality constraints.
        self.query = self.reduce_equality_constraints(self.query)

        check_is_it_safe()

        select_clause = 'SELECT ' + ','.join(getSelectedColumns())
        from_clause = 'FROM bla'
        where_clause = 'WHERE ' + ','.join(getExplicitConstraints(), getImplicitConstraints(), getJoinConstraints())

        return select_clause + from_clause + where_clause
