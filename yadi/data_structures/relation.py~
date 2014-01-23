class RelationInQuery:

    def __init__(self, name='', variables={},constants = {},wildcards = [], is_negated = False):
        self.name = name # The name of the relation
        self.variables = variables # {Variable -> [Position]}
        self.constants = constants # {Constant -> [Position]}
        self.is_negated = is_negated # Is it negated
        self.wildcards = wildcards # [position]
    def __repr__(self):
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

    def get_name(self):
        return self.name

    def get_variables(self):
        return self.variables

    def get_constants(self):
        return self.constants

    def get_wildcards(self):
        return self.wildcards

    def is_negated(self):
        return is_negated

    def get_ordered_element_list(self):

        order_dict = {}

        variables = self.get_variables()
        for var in variables.keys():
            for pos in variables[var]:
                order_dict[pos] = var

        constants = self.get_constants()
        for const in constants:
            for pos in constants[const]:
                order_dict[pos] = const


        for pos in self.get_wildcards():
            order_dict[pos] = '_'
    
        return [order_dict[index] for index in range(0,len(order_dict)]
