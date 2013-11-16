import copy
from dataStructures.query import *
from dataStructures.constraint import *

class QueryPreprocessor():
    def preprocess(self,query):
        if isinstance(query, ConjunctiveQuery):
            pp = ConjunctiveQueryPreprocessor()
        if isinstance(query, DisjunctiveQuery):
            pp = DisjunctiveQueryPreprocessor()
        return pp.preprocess(query)

class ConjunctiveQueryPreprocessor():

    def preprocess(self,query):
        query = self.reduce_equality_constraints(query)
        return query

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
