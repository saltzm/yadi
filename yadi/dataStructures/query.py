class Query():
    def get_relations(self):
        pass

class DisjunctiveQuery(Query):
    def __init__(self, queries = []):
        self.queries = queries

    def get_queries(self):
        return self.queries

    def get_relations(self):
        return [x.get_relations for x in self.get_queries()]


class ConjunctiveQuery(Query):
    def __init__(self, relations = [], constraints = [], head_relation = None):
        self.head_relation = head_relation
        self.relations = relations      # [RelationInQuery].
        self.constraints = constraints  # Explicit constraints of the form
                                        # Element COMP Element type.
                                        # [Constraint]

    def set_head_relation(self,hr):
        self.head_relation = hr

    def get_head_relation(self):
        return self.head_relation

    def get_relations(self):
        return self.relations

    def get_constraints(self):
        return self.constraints

    def __repr__(self):

        return str(self.head_relation) + ':-' + \
               ','.join([str(x) for x in self.relations]) + \
               (',' if len(self.constraints)>0 else '') + \
               ','.join([str(x) for x in self.constraints])

    # var_dict is a Variable -> [(Relation, field)] which is usefuld for several purposes.
    # It does not map occurences of variables in negated goals.
    def get_var_dict(self):
        variables_in_positive_goals = [y for x in self.relations for y in x.variables if not x.is_negated()]
        var_dict = {}

        for relation in [x for x in self.relations if not x.is_negated()]:
            for var in relation.variables:
                if not var in var_dict:
                    var_dict[var] = []
                for position in relation.variables[var]:
                    var_dict[var].append((relation,position))

        return var_dict

