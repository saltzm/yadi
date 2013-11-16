class RelationInQuery:

    def __init__(self, name='', variables={},constants = {},wildcards = [], negated = False):
        self.name = name # The name of the relation
        self.variables = variables # {Variable -> [Position]}
        self.constants = constants # {Constant -> [Position]}
        self.negated = negated # Is it negated
        self.wildcards = wildcards # [position]

    def __init__(self, name='', elements = [],negated = False):
        self.name = name
        self.negated = negated # Is it negated

        self.variables = {} # {Variable -> [Position]}
        self.constants = {} # {Constant -> [Position]}
        self.wildcards = [] # Is it negated

        for element in elements:
            if element.is_variable():
                self.variables[element] = []
            if element.is_constant():
                self.constants[element] = []

        # Build the variables, constants dictionaries and the wildcard list.
        for i in range(0,len(elements)):
            element = elements[i]
            if element.is_variable():
                self.variables[element].append(i)
            if element.is_constant():
                self.constants[element].append(i)
            if element.is_wildcard():
                self.wildcards.append(i)        

    def __repr__(self):
        list_of_columns = list(range(0,len([y for x in self.variables.values() for y in x]) + \
                                  len([y for x in self.constants.values() for y in x]) + \
                                  len(self.wildcards)))

        for variable in self.variables:
            for position in self.variables[variable]:
                list_of_columns[position] = str(variable)
        for constant in self.constants:
            for position in self.constants[constant]:
                 list_of_columns[position] = str(constant)
        for position in self.wildcards:
            list_of_columns[position] = '_'

        neg_str = '!' if self.negated else ''

        return neg_str + self.name + '('+','.join(list_of_columns)+')'

    def get_name(self):
        return self.name

    def set_name(self,name):
        self.name = name

    def get_variables(self):
        return self.variables

    def get_constants(self):
        return self.constants

    def get_wildcards(self):
        return self.wildcards

    def is_negated(self):
        return self.negated

    def get_ordered_element_list(self):

        order_dict = {}

        variables = self.get_variables()
        for var in variables:
            for pos in variables[var]:
                order_dict[pos] = var

        constants = self.get_constants()
        for const in constants:
            for pos in constants[const]:
                order_dict[pos] = const


        for pos in self.get_wildcards():
            order_dict[pos] = '_'

        return [order_dict[index] for index in range(0,len(order_dict))]
