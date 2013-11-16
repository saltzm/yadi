class SQLGenerator():
    def get_SQL_code(self,query):
        if isinstance(query, ConjunctiveQuery):
            sql_gen = ConjunctiveQuerySQLGenerator()
        if isinstance(query, DisjunctiveQuery):
            sql_gen = DisjunctiveQuerySQLGenerator()
        return cq_sql_gen.get_SQL_code(query)

class DisjunctiveQuerySQLGenerator():

    def get_SQL_code(self,query):
        sql_gen = SQLGenerator()
        ' UNION '.join([sql_gen.get_SQL_code(q) for q in query.get_queries()]) 

class ConjunctiveQuerySQLGenerator():

    def create_var_dict(self,query):
        var_dict = {}

        for relation in [r for r in query.get_relations() if not r.is_negated()]:
            for var in relation.variables.keys():
                if not var_dict.has_key(var):
                    var_dict[var] = []
                for position in relation.variables[var]:
                    var_dict[var].append((relation,position))

        return var_dict

    def get_SQL_code(self,query):

        var_dict = self.create_var_dict(query)

        return 'SELECT ' + ','.join(self.get_select_columns()) + \
               'FROM ' + ','.join(self.get_from_relations()) + \
               'WHERE' + ' AND '.join(self.get_implicit_constraints(query.get_relations())) + \
                         ' AND '.join(self.get_join_constraints(var_dict)) + \
                         ' AND '.join(self.get_explicit_constraints(query.get_constraints(),var_dict)) + \
                         ' AND '.join(self.get_negated_queries())   

    def mapVariableToRelationDotPosition(self,var,var_dict,pos = 0):
        relation = var_dict[var][pos][0]
        position = var_dict[var][pos][1]
        return self.relation.get_name() + '.' + self.mapPositionToColumnName(relation,position)

    
    def mapPositionToColumnName(self,relation,position):
        return '_' + position

    def get_select_columns(self):
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


    def get_implicit_constraints(self,relations):
        ''' An implicit constraint is one in which you are unifying a constant to a position of the relation
            E.G. R(X,2) specifies that R.2 == 2'''

        constraints = []
        for relation in relations:
            const_dict = relation.get_constants()
            for constant in const_dict.get_keys():
                for position in const_dict[constant]:
                    constraints.append(relation.get_name()+'.'+ str(position) + '=' + str(constant))
        return constraints

    def get_explicit_constraints(self,constraints,var_dict):
        ''' An explicit constraint is one of the form Element COMP Element type, explicitly listed in the conjunctive query
            E.G. R(X,Y), Y>2 specifies that R.2 > 2'''

        constraints = []
        for constraint in constraints:
            if constraint.get_left_side().is_variable(): 
                left_side = self.mapVariableToRelationDotPosition(constraint.get_left_side(),var_dict)
            else:
                left_side = str(constraint.get_left_side())

            if constraint.get_right_side().is_variable():
                right_side = self.mapVariableToRelationDotPosition(constraint.get_right_side(),var_dict)
            else:
                right_side = str(constraint.get_right_side())

            constraints.append(left_side + str(constraint.get_operator()) + right_side)

        return constraints

    def get_join_constraints(self,var_dict):
        constraints = []
        for var in var_dict.keys():
            length = len(var_dict[var])
            for i in range(1,length):
                constraints.append(mapVariableToRelationDotPosition(var,var_dict,0) + '=' + mapVariableToRelationDotPosition(var,var_dict,i))
        return constraints

    def get_negated_queries(self,relations,var_dict):
        negated_queries_sql = []
        for relation in [r for r in relations if r.is_negated()]:
            where_clauses = []
            elements = relation.get_ordered_element_list()
            for position in range(0,len(elements)):
                element = elements[position]
                var =  relation.get_name() + '.' + self.mapPositionToColumnName(relation,position) 
                if isinstance(element,Variable):
                    where_clauses.append(var + '=' + mapVariableToRelationDotPosition(element,var_dict))
                elif isinstance(element,Constant):
                    where_clauses.append(var + '=' + str(element))

            negated_queries_sql.append('NOT EXISTS (SELECT * FROM ' +  relation + 'WHERE' +'AND'.join(where_clauses) + ')')

        return negated_queries_sql

