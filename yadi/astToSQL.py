#TODO: 

# Check the IS EQUALITY or IS IS COMPARISON in check_is_it_safe() (there's 2 things to check).
# Implement check variables that occur in defined predicates.

import copy

equality_operator = '='

class NotSafeException(Exception):
    pass
class NotInstantiatedException(Exception):
    pass

class Element:
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.__dict__ == other.__dict__)
    def is_variable(self): 
        return isinstance(self,Variable)
    def is_constant(self): 
        return isinstance(self,Constant)

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

class Constraint():
    EQ_OPERATOR = '='
    def __init__(self, left_side, right_side, operator):
        self.left_side = left_side
        self.right_side = right_side
        self.operator = operator

    def is_equality_constraint(self):
        return self.operator == Constraint.EQ_OPERATOR

    def get_left_side(self):
        return self.left_side

    def get_right_side(self):
        return self.right_side

    def get_operator(self):
        return self.operator

    def set_left_side(self,el):
        self.left_side = el

    def set_right_side(self,el):
        self.right_side = el

    def __repr__(self):
        return str(self.get_left_side()) + str(self.get_operator()) + str(self.get_right_side())

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
        '''return ('name: ' + self.name + '\n' + 
               'variables: ' + str(self.variables) + '\n' +
               'constants: ' + str(self.constants) + '\n' + 
               'is_negated: ' + str(self.is_negated) + '\n' +
               'wildcards: ' + str(self.wildcards) + '\n')'''

        list_of_columns = range(0,len([y for x in self.variables.values() for y in x]) + \
                                  len([y for x in self.constants.values() for y in x]) + \
                                  len(self.wildcards))

        for variable in self.variables.keys():
            for position in self.variables[variable]:
                list_of_columns[position] = str(variable)
        for constant in self.constants.keys():
            for position in self.constants[constant]:
                 list_of_columns[position] = str(constant)
        for position in self.wildcards:
            list_of_columns[position] = '_'

        negated = '!' if self.is_negated else ''

        return negated + self.name + '('+','.join(list_of_columns)+')'

    def get_names(self):
        return self.variables

    def get_variables(self):
        return self.variables

    def get_constants(self):
        return self.constants

    def get_wildcards(self):
        return self.wildcards

class DisjunctiveQuery:
    def __init__(self, conjunctive_queries = []):
        self.conjunctive_queries = conjunctive_queries

class ConjunctiveQuery:
    def __init__(self, relations = [], constraints = [], head_relation = None):
        self.head_relation = head_relation
        self.relations = relations# [RelationInQuery].
        self.constraints = constraints # Explicit constraints of the form Element COMP Element type.
                                       # [Constraint]

    def __repr__(self):
        '''return ('Head vars: ' + str(self.head_variables) + str(self.head_constants) + '\n'+ 'Relations: ' + str(self.relations) + '\n' + 'Constraints: '+ str(self.constraints))# )'''
        string = 'R('
        list_of_columns = range(0,len([y for x in self.head_relation.get_variables().values() for y in x]) + \
                                  len([y for x in self.head_relation.get_constants().values() for y in x]))

        for head_variable in self.head_relation.get_variables().keys():
            for position in self.head_relation.get_variables()[head_variable]:
                list_of_columns[position] = str(head_variable)

        for head_constant in self.head_relation.get_constants().keys():
            for position in self.head_relation.get_constants()[head_constant]:
                list_of_columns[position] = str(head_constant)

        return str(self.head_relation)+':-'+','.join([str(x) for x in self.relations]) + (',' if len(self.constraints)>0 else '') + ','.join([str(x) for x in self.constraints])
            


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
            if constraint.get_left_side().is_variable(): 
                left_side = self.var_dict[constraint.get_left_side()][0].name+'.'+self.var_dict[constraint.get_left_side()][1]
            else:
                left_side = constraint.get_left_side().value

            if constraint.get_right_side().is_variable():
                right_side = self.var_dict[constraint.get_right_side()][0].name+'.'+self.var_dict[constraint.get_right_side()][1]
            else:
                right_side = constraint.get_right_side().value

            constraints.append(left_side + constraint.get_operator() + right_side)

        return constraints

    def getSelectedColumns(self):
        list_of_columns = range(0,len([y for x in self.query.head_relation.get_variables().values() for y in x]) + \
                                  len([y for x in self.query.head_relation.get_constants().values() for y in x]))

        for head_variable in self.query.head_relation.get_variables().keys():
            for position in self.query.head_relation.get_variables()[head_variable]:
                if self.var_dict.has_key(head_variable):
                    list_of_columns[position] = str(self.var_dict[head_variable][0][0].name) + '._' + str(self.var_dict[head_variable][0][1]) + ' as ' + str(head_variable.name)
                else: # There is no occurence of head_variable in a relation, so it must be in a constraint
                    constraint = [x for x in self.query.constraints if (x.get_left_side() == head_variable and x.is_equality_constraint())][0]
                    list_of_columns[position] = str(constraint.get_right_side()) + ' as _'+str(position)                 
        for head_constant in self.query.head_relation.get_constants().keys():
            for position in self.query.head_relation.get_constants()[head_constant]:
                list_of_columns[position] = head_constant.value + ' as _'+str(position)
        
        return list_of_columns    


    def getNotExistsClauses(self):
        for relation in self.query.relations:
            if relation.negated:
                for variable in relation.variables:
                    pass

    def get_safe_variables(self):
        # Create a list of safe variables: variables bounded to constants or that occur in a positive goal

        variables_bounded_to_constants = []

        for constraint in self.query.constraints:
            if (constraint.get_left_side().is_variable() and 
                constraint.get_right_side().is_constant() and 
                constraint.is_equality_constraint()): 
                    variables_bounded_to_constants.append(constraint.get_left_side())

        safe_variables = self.var_dict.keys() + variables_bounded_to_constants

        return safe_variables

    def check_is_it_safe(self):
        safe_variables = self.get_safe_variables()

        return (self.check_head(safe_variables) and 
               self.check_negated_goals(safe_variables) and 
               self.check_non_equality_explicit_constraints(safe_variables))

    def check_head(self,safe_variables):

        for variable in self.query.head_relation.get_variables().keys():
            if not (variable in safe_variables):
                raise NotSafeException('Query not safe because '+ variable.name + ' occurs in the head and not in a positive goal')
                return False
        return True

    def check_negated_goals(self,safe_variables):

        # Create a list of variables which occur in negated goals. 
        variables_in_negated_goals = [y for x in self.query.relations for y in x.variables.keys() if x.is_negated] 

        # And check them:
        for variable in variables_in_negated_goals:
            if not (variable in safe_variables):
                raise NotSafeException('Query not safe because ' + variable.name + ' from a negated goal does not occur in a positive goal')
                return False

        return True


    def check_non_equality_explicit_constraints(self,safe_variables):

        # Checking variables which occur in explicit constraints with non equality operators

        # Create a list of variables which occur in explicit constraints with non equality operators
        variables_in_constraints_with_non_equality_operators = [y for x in self.query.constraints \
                                                                    for y in [x.get_left_side(),x.get_right_side()] \
                                                                        if y.is_variable() and not x.is_equality_constraint()]

        for variable in variables_in_constraints_with_non_equality_operators:
            if not (variable in safe_variables):
                raise NotSafeException('Query not safe because ' + variable.name + ' from a non_equality comparison does not occur in a positive goal')
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
        # Build the equivalence sets

        equality_constraints = [x for x in query.constraints if x.is_equality_constraint()]
        eq_sets = []
        for eq_constraint in equality_constraints:
            el1 = eq_constraint.get_left_side()
            el2 = eq_constraint.get_right_side()
            
            set1 = -1
            set2 = -1
                
            for i in range(0,len(eq_sets)):
                if el1 in eq_sets[i]:
                    set1 = i
                if el2 in eq_sets[i]:
                    set2 = i

            if set1== -1 and set2== -1: # Neither El1 nor El2 is in a set.
                eq_sets.append({el1,el2})
            else: # set1 >= 0 OR set2>=0
                if set1>= 0:
                    if set2 == -1: # El1 is in some set and El2 is not.
                        eq_sets[set1].add(el2)
                    else: # El1 and El2 are both in some sets.
                        if set1!=set2: # If they're not in the same set, merge them and delete one of them.
                            eq_sets[set1] = eq_sets[set1] | eq_sets[set2]
                            eq_sets.remove(eq_sets[set2])
                else:
                    if set2 >= 0: # El2 is in a set, El1 is not.
                        eq_sets[set2].add(el1)

        new_eq_constraints = []

        for s in eq_sets:
            constants = [x for x in s if x.is_constant()]
            variables = [x for x in s if x.is_variable()]
            variables_occur_relation = [y for x in query.relations for y in x.variables.keys() if y in variables] 

            if len(variables_occur_relation)==0 and len(variables)>0 :
                raise NotInstantiatedException('Equivalence set of ' + str(variables[0]) + ' does not unify with a variable in a positive' )
            
            # Substitute every variable in the equivalence set b 
            if len(constants)>0: 
                # Substitute every occurence of variable in every goal with the constant
                constant = constants[0]
                for relation in query.relations:
                    del_list = []

                    for variable in relation.variables:
                        if variable in s:
                            if relation.constants.has_key(constant):
                                relation.constants[constant] += relation.variables[variable]
                            else:
                                relation.constants[constant] = relation.variables[variable]
                            del_list.append(variable)
                    for variable in del_list:
                        del relation.variables[variable]

                # Substitute every occurence of the variable in the constraints with the constant
                for constraint in query.constraints:
                    el0 = constraint.get_left_side()
                    el1 = constraint.get_right_side()
                    if el0.is_variable() and el0 in s:
                        constraint.set_left_side(constant)
                    if el1.is_variable() and el1 in s:
                        constraint.set_right_side(constant)
                # Make sure we can still unify head variables with constants if they are in the equivalence set.
                for variable in variables:
                    if variable in query.head_relation.get_variables().keys():
                        new_eq_constraints.append(Constraint(variable,constant,Constraint.EQ_OPERATOR))                              
            else:
                # Substitute every occurence of variable in the relations with one variable from variables_occur_relation
                var = variables_occur_relation[0]
                for relation in query.relations:
                    del_list = []
                    add_dict = {}
                    for variable in relation.variables:
                        if variable in s and (not variable == var):
                            if relation.variables.has_key(var):
                                relation.variables[var] += relation.variables[variable]
                            else:
                                add_dict[var] = relation.variables[variable]
                            del_list.append(variable)
                    for variable in del_list:
                        del relation.variables[variable]

                    for key in add_dict.keys():
                        relation.variables[key] = add_dict[key]
                # Substitute every occurence of variable in the head with one variable from variables_occur_relation

                variables_in_head = query.head_relation.get_variables().keys()
                if not query.head_relation.get_variables().has_key(var):
                    query.head_relation.get_variables()[var] = []

                for head_var in variables_in_head:
                    if head_var in s and not var == head_var:
                        query.head_relation.get_variables()[var] += query.head_relation.get_variables().pop(head_var)

                # Substitute every occurence of variable in the constraints with one variable from variables_occur_relation
                for constraint in query.constraints:
                    el0 = constraint.get_left_side()
                    el1 = constraint.get_right_side()
                    if el0.is_variable() and el0 in s:
                        constraint.set_left_side(var)
                    if el1.is_variable() and el1 in s:
                        constraint.set_right_side(var)

            # If there's more than one constant in this equivalence set, they are all be different so we need to keep one of these constraints so the query returns false.
            if len(constants)>1:
                new_eq_constraints.append(Constraint(constants[0],constants[1],Constraint.EQ_OPERATOR))                                

        query.constraints = [x for x in query.constraints if not x.is_equality_constraint()] + new_eq_constraints
        return query

 
    def preProcessQuery(self,query):
        query = self.reduce_equality_constraints(query)
        self.var_dict = self.create_var_dict(query) 
        return query

    def generateAlchemyStatement(self):

        # We modify the query object by removing unnecesary equality constraints.
        self.query = self.preProcessQuery(self.query)
        self.check_is_it_safe()
        return 'SELECT ' + ','.join(self.getSelectedColumns())
'''
        select_clause = 'SELECT ' + ','.join(getSelectedColumns())
        from_clause = 'FROM bla'
        where_clause = 'WHERE ' + ','.join(getExplicitConstraints(), getImplicitConstraints(), getJoinConstraints())

        return select_clause + from_clause + where_clause'''
