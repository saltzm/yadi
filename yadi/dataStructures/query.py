class Query():
    def get_relations():
        pass

'''
class NegatedQuery(Query):
    def __init__(self, relation = None):
        self.relation = relation

    def get_relations():
        return [self.relation]
'''

class DisjunctiveQuery(Query):
    def __init__(self, queries = []):
        self.queries = queries

    def get_queries(self):
        return self.queries

    def get_relations():
        return [x.get_relations for x in self.get_queries()]


class ConjunctiveQuery(Query):
    def __init__(self, relations = [], constraints = [], head_relation = None):
        self.head_relation = head_relation
        self.relations = relations      # [RelationInQuery].
        self.constraints = constraints  # Explicit constraints of the form
                                        # Element COMP Element type.
                                        # [Constraint]

    def get_relations(self):
        return self.relations

    def get_constraints(self):
        return self.constraints

    def __repr__(self):
        string = 'R('
        list_of_columns = range(0,len([y for x in self.head_relation.get_variables().values() for y in x]) + \
                                  len([y for x in self.head_relation.get_constants().values() for y in x]))

        for head_variable in self.head_relation.get_variables().keys():
            for position in self.head_relation.get_variables()[head_variable]:
                list_of_columns[position] = str(head_variable)

        for head_constant in self.head_relation.get_constants().keys():
            for position in self.head_relation.get_constants()[head_constant]:
                list_of_columns[position] = str(head_constant)

        return str(self.head_relation) + ':-' + \
               ','.join([str(x) for x in self.relations]) + \
               (',' if len(self.constraints)>0 else '') + \
               ','.join([str(x) for x in self.constraints])

