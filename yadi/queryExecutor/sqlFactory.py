from ..dataStructures.query import *

class SQLGenerator():
    def get_SQL_code(self,query,old_query):
        if isinstance(query, ConjunctiveQuery):
            sql_gen = ConjunctiveQuerySQLGenerator()
        if isinstance(query, DisjunctiveQuery):
            sql_gen = DisjunctiveQuerySQLGenerator()
        return sql_gen.get_SQL_code(query,old_query)

class DisjunctiveQuerySQLGenerator():

    def get_SQL_code(self,query,old_query):
        sql_gen = SQLGenerator()
        ' UNION '.join([sql_gen.get_SQL_code(q) for q in query.get_queries()])

class ConjunctiveQuerySQLGenerator():

    def get_SQL_code(self,query,old_query,pretty_print=False):
        aliases = self.create_table_aliases(query)
        var_dict = query.get_var_dict()

        select_clause = self.get_select_columns(query.get_head_relation(), query.get_constraints(), var_dict, old_query.get_head_relation())
        from_clause = self.get_from_relations(query,aliases)
        implicit_constraints = self.get_implicit_constraints(query.get_relations())
        join_constraints = self.get_join_constraints(var_dict)
        explicit_constraints = self.get_explicit_constraints(query.get_constraints(),var_dict)
        negated_queries = self.get_negated_queries(query.get_relations(),var_dict)
        where_separator = ' AND \n\t' if pretty_print else ' AND '
        where_clause = where_separator.join(implicit_constraints + join_constraints + explicit_constraints + negated_queries)
        if pretty_print:
            return 'SELECT \n\t' + ', \n\t'.join(select_clause) + \
               ('\nFROM \n\t' if len(from_clause) != 0 else '') + \
               ', \n\t'.join(from_clause) + \
               ('\nWHERE \n\t' if len(where_clause) != 0 else '') + where_clause + ';'
        else:
            return 'SELECT ' + ', '.join(select_clause) + \
               (' FROM ' if len(from_clause) != 0 else '') + \
               ', '.join(from_clause) + \
               (' WHERE ' if len(where_clause) != 0 else '') + where_clause + ';'



    def create_table_aliases(self,query):
        count = {}
        for relation in query.get_relations():
            if not (relation.get_name() in count):
                count[relation.get_name()] = 0
            else:
                count[relation.get_name()]+=1

        aliases = {}

        repeated_relations = [relation for relation in query.get_relations() if count[relation.get_name()]>0]
        non_repeated_relations = [relation for relation in query.get_relations() if count[relation.get_name()]==0]

        for relation in repeated_relations:
            old_name = relation.get_name()
            relation.set_name(old_name+str(count[relation.get_name()]))
            count[old_name]-=1
            aliases[relation.get_name()] = old_name + ' as ' + relation.get_name()

        for relation in non_repeated_relations:
            aliases[relation.get_name()] = relation.get_name()

        return aliases

    def mapVariableToRelationDotField(self,var,var_dict,pos = 0):
        relation = var_dict[var][pos][0]
        position = var_dict[var][pos][1]
        return relation.get_name() + '.'+ self.mapPositionToColumnName(relation,position)

    def get_from_relations(self, query,aliases):
        '''
        Returns list of the names of all positive relations in the query
        '''
        return [aliases[rel.get_name()] for rel in query.get_relations() if not rel.is_negated()]

    def mapPositionToColumnName(self,relation,position):
        return '_' + str(position)

    def get_select_columns(self,head_relation,constraints,var_dict, original_head_relation):
        column_list = []

        element_list = head_relation.get_ordered_element_list()

        if len(element_list) == 0:
            column_list = ["'TRUE'"]
        else:
            if original_head_relation is None:
                as_names = head_relation.get_ordered_element_list()
            else:
                as_names = original_head_relation.get_ordered_element_list()
            for i in range(0,len(element_list)):
                element = element_list[i]
                if element.is_variable():
                    if element in var_dict:
                    # It's in a positive goal.
                        column_list.append(self.mapVariableToRelationDotField(element, var_dict) + ' as ' + str(as_names[i]))
                    else:# It is a constant (it appears in a constraint).
                        const = str([x.get_right_side() for x in constraints if (x.get_left_side() == element and x.is_equality_constraint())][0])
                        column_list.append(const + ' as ' + str(as_names[i]))
                if element.is_constant():
                    column_list.append(str(element))
                if element.is_wildcard():
                    pass


        return column_list

    def get_implicit_constraints(self,relations):
        ''' An implicit constraint is one in which you are unifying a constant to a position of the relation
            E.G. R(X,2) specifies that R.2 == 2'''

        constraints = []
        for relation in [r for r in relations if not r.is_negated()]  :
            const_dict = relation.get_constants()
            for constant in const_dict:
                for position in const_dict[constant]:
                    constraints.append( \
                        relation.get_name() + '.' + self.mapPositionToColumnName(relation,position) + ' = ' + str(constant) \
                    )
        return constraints

    def get_explicit_constraints(self,constraints,var_dict):
        '''
        Returns SQL representation of an explicit constraint. An explicit
        constraint is one of the form Element COMP Element type, explicitly
        listed in the conjunctive query. E.G. R(X,Y), Y>2 specifies that R.2 > 2
        '''

        constraints_strings = []
        for constraint in constraints:
            ls = constraint.get_left_side()
            rs = constraint.get_right_side()

            if not (ls.is_variable() and constraint.is_equality_constraint()):
                ''' Every Var = Constant constraint where var is only in head. We don't want this type of constraints.
                    We assume that if there is a Var = Constraint, var occurs in the head. Otherwise it would be unified in the preprocessor.
                '''
                if ls.is_variable():
                    left_side = self.mapVariableToRelationDotField(ls, var_dict)
                elif ls.is_constant():
                    left_side = str(ls)

                if rs.is_variable():
                    right_side = self.mapVariableToRelationDotField(rs, var_dict)
                elif rs.is_constant():
                    right_side = str(rs)

                constraints_strings.append(
                    str(left_side) + ' ' + str(constraint.get_operator()) + ' ' + str(right_side)
                )

        return constraints_strings

    def get_join_constraints(self,var_dict):
        constraints = []

        for var in var_dict:
            length = len(var_dict[var])
            for i in range(1,length):
                constraints.append(
                    self.mapVariableToRelationDotField(var,var_dict,0) +
                    ' = ' +
                    self.mapVariableToRelationDotField(var,var_dict,i)
                )
        return constraints

    def get_negated_queries(self,relations,var_dict):
        negated_queries_sql = []
        for relation in [r for r in relations if r.is_negated()]:
            where_clauses = []
            elements = relation.get_ordered_element_list()

            for position in range(0,len(elements)):
                element = elements[position]
                var =  relation.get_name() + '.' + \
                       self.mapPositionToColumnName(relation, position)

                if element.is_variable():
                    where_clauses.append(
                        var + ' = ' +
                        self.mapVariableToRelationDotField(element, var_dict)
                    )
                elif element.is_constant():
                    where_clauses.append(var + ' = ' + str(element))

            negated_queries_sql.append(
                'NOT EXISTS (' +
                    'SELECT * FROM ' + relation.get_name() +
                    ' WHERE ' + ' AND '.join(where_clauses) +
                ')'
            )

        return negated_queries_sql

