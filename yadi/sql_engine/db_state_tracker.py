
class DBStateTracker:
    def __init__(self, query_evaluator, persistence = False):
        self.query_evaluator = query_evaluator
        self.asserted_queries = {} # list of AssertedQuery objects with
                                   # head_relation as key
        self.persistence = persistence

    def add_assertion(self, query):
        query_name = query.get_query().get_head_relation().get_name()
        if query_name in self.asserted_queries:
            assert self.heads_match(self.asserted_queries[query_name][0],
                    query), 'views with the same name must have the same arity'

            self.asserted_queries[query_name] += [query]
        else:
            self.asserted_queries[query_name] = [query]

    def heads_match(self, q1, q2):
       h1_vars = q1.get_query().get_head_relation().get_variables().values()
       h1_arity = sum([len(x) for x in h1_vars])
       h2_vars = q2.get_query().get_head_relation().get_variables().values()
       h2_arity = sum([len(x) for x in h2_vars])
       return h1_arity == h2_arity

    def get_assertions(self, name):
        return self.asserted_queries[name]

    def contains_assertion(self, name):
        return name in self.asserted_queries

    def __del__(self):
        # Perform rollbacks on views
        if not self.persistence:
            self.perform_rollbacks()

    def perform_rollbacks(self):
        for a in self.asserted_queries:
            self.query_evaluator.execute('DROP VIEW IF EXISTS ' + a + ' CASCADE;')
