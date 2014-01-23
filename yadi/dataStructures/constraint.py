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

