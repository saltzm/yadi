from ..query_data_structures.query import *
from ...sql_engine.db_state_tracker import DBStateTracker

class SQLGenerator:
    def __init__(self, db_state_tracker):
        self.db_state_tracker = db_state_tracker

    def get_SQL_code(self,query,old_query):
        if isinstance(query, ConjunctiveQuery):
            sql_gen = ConjunctiveQuerySQLGenerator(self.db_state_tracker)
        if isinstance(query, DisjunctiveQuery):
            sql_gen = DisjunctiveQuerySQLGenerator(self.db_state_tracker)
        if isinstance(query, AssertedQuery):
            sql_gen = AssertedQuerySQLGenerator(self.db_state_tracker)

        return sql_gen.get_SQL_code(query, old_query)

class AssertedQuerySQLGenerator:
    def __init__(self, db_state_tracker):
        self.db_state_tracker = db_state_tracker

    def get_SQL_code(self, query, old_query):
        if old_query.is_fact:
            return self.get_fact_code(query)
        else:
            return self.get_rule_code(query, old_query)

    def get_fact_code(self, query):
        assert len(query.get_query().get_relations()) == 1
        rel = query.get_query().get_relations()[0]
        assert len(rel.get_variables()) == 0
        rel_name = rel.get_name()
        column_list = '(' + ', '.join(['_' + str(i) + ' VARCHAR(500) '
                            for i in range(0, len(rel.get_constants()))]) + ')'
        constants = rel.get_constants()
        list_of_columns = \
            list(range(0, len([y for x in constants.values() for y in x])))

        for constant in constants:
            for position in constants[constant]:
                 list_of_columns[position] = str(constant)

        values = '(' + ', '.join([str(x) for x in list_of_columns]) + ');'

        return 'CREATE TABLE IF NOT EXISTS ' + rel_name + ' ' + column_list + '; ' + \
               'INSERT INTO ' + rel_name + ' VALUES ' + values

    def get_rule_code(self, query, old_query):
        sql_gen = SQLGenerator(self.db_state_tracker)
        query_sql = sql_gen.get_SQL_code(query.get_query(),
                old_query.get_query())
        head_relation = query.get_query().get_head_relation()
        view_name = query.get_query().get_head_relation().get_name()
        head_vars = query.get_query().get_head_relation().get_variables()
        drop_sql = ''

        i = 0
        for var in head_vars:
            for col in range(0, len(head_vars[var])):
                query_sql = query_sql.replace(' AS ' + str(var), ' AS ' + '_' +
                        str(i), 1)
                i = i + 1

        # Check if this view already exists in the db_state_tracker
        if self.db_state_tracker.contains_assertion(view_name):
            # Retrieve existing_assertion
            existing_assertions = self.db_state_tracker.get_assertions(view_name)
            for a in existing_assertions:
                # Get sql code from existing_assertion's inner query
                existing_query_sql = \
                    SQLGenerator(self.db_state_tracker).get_SQL_code(a.get_query(),
                            a.get_query())
                i = 0
                existing_head_vars = a.get_query().get_head_relation().get_variables()
                for var in existing_head_vars:
                    for col in range(0, len(existing_head_vars[var])):
                        existing_query_sql = existing_query_sql.replace(' AS ' +
                                str(var), ' AS ' + '_' + str(i), 1)
                        i = i + 1

                query_sql = query_sql[:-1] + ' UNION ' + existing_query_sql
            # Create rollback code
            drop_sql = self.get_rollback_code(query) + ' '

        # Add new query to db_state_tracker
        self.db_state_tracker.add_assertion(query)

        head_vals = head_vars.values()
        head_arity = sum([len(x) for x in head_vals])
        columns = ' (' + ', '.join(['_' + str(i) for i in range(0, head_arity)]) + ') '

        return drop_sql + 'CREATE VIEW ' + view_name + ' AS ' + query_sql + ';'
#        return drop_sql + 'CREATE RECURSIVE VIEW ' + view_name + columns + \
#                ' AS ' + query_sql + ';'
#            ' AS WITH RECURSIVE ' + view_name + columns + ' AS ' + query_sql + ';'

    def get_rollback_code(self, query):
        return 'DROP VIEW IF EXISTS ' + query.get_query().head_relation.get_name() + ';'

class DisjunctiveQuerySQLGenerator:
    def __init__(self, db_state_tracker):
        self.db_state_tracker = db_state_tracker

    def get_SQL_code(self,query,old_query):
        sql_gen = SQLGenerator(self.db_state_tracker)
        old_queries = old_query.get_queries()
        new_queries = query.get_queries()
        old_new_pairs = [(new_queries[aux], old_queries[aux]) for aux in range(0,len(new_queries))]
        return ' UNION '.join(['(' + sql_gen.get_SQL_code(q, old_q)[:-1] + ')' for (q, old_q) in old_new_pairs]) +';'


class ConjunctiveQuerySQLGenerator:
    def __init__(self, db_state_tracker):
        self.db_state_tracker = db_state_tracker

    def get_SQL_code(self,query,old_query,pretty_print=False):
        aliases = self.create_table_aliases(query)
        var_dict = query.get_var_dict()

        select_clause = self.get_select_columns(query.get_head_relation(),
                                                query.get_constraints(),
                                                var_dict,
                                                old_query.get_head_relation())
        from_clause = self.get_from_relations(query,aliases)
        implicit_constraints = self.get_implicit_constraints(query.get_relations())
        join_constraints = self.get_join_constraints(var_dict)
        explicit_constraints = self.get_explicit_constraints(
                                    query.get_constraints(),
                                    var_dict)
        negated_queries = self.get_negated_queries(query.get_relations(),
                var_dict, aliases)
        where_separator = ' AND \n\t' if pretty_print else ' AND '
        where_clause = where_separator.join(
            implicit_constraints +
            join_constraints +
            explicit_constraints +
            negated_queries
        )
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
                count[relation.get_name()] += 1

        aliases = {}

        repeated_relations = [relation for relation in query.get_relations() if count[relation.get_name()]>0]
        non_repeated_relations = [relation for relation in query.get_relations() if count[relation.get_name()]==0]

        for relation in repeated_relations:
            old_name = relation.get_name()
            relation.set_name(old_name+str(count[relation.get_name()]))
            count[old_name]-=1
            aliases[relation.get_name()] = old_name + ' AS ' + relation.get_name()

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

        element_list = head_relation.get_ordered_element_list

        if len(element_list) == 0:
            column_list = ["CASE COUNT(*) WHEN 0 THEN 'FALSE' ELSE 'TRUE' END"]
        else:
            if original_head_relation is None:
                as_names = head_relation.get_ordered_element_list
            else:
                as_names = original_head_relation.get_ordered_element_list
            for i in range(0,len(element_list)):
                element = element_list[i]
                if element.is_variable():
                    if element in var_dict:
                    # It's in a positive goal.
                        column_list.append(self.mapVariableToRelationDotField(element,
                            var_dict) + ' AS ' + str(as_names[i]))
                    else:# It is a constant (it appears in a constraint).
                        const = str([x.get_right_side() for x in constraints if (x.get_left_side() == element and x.is_equality_constraint())][0])
                        column_list.append(const + ' AS ' + str(as_names[i]))
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

    def get_negated_queries(self, relations, var_dict, aliases):
        negated_queries_sql = []
        for relation in [r for r in relations if r.is_negated()]:
            where_clauses = []
            elements = relation.get_ordered_element_list

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
                    'SELECT * FROM ' + aliases[relation.get_name()] +
                    ' WHERE ' + ' AND '.join(where_clauses) +
                ')'
            )

        return negated_queries_sql
