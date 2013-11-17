from pyparsing import *

# TODO: 1. Implement nested joins.
# TODO: 2. Look at LJ, RJ, FJ grouping. Get to some agreement on this.
# TODO: 3. Implement Datalog function (top, etc.) checking to be the FIRST thing to be evaluated in rule expression.

# Notes:
# - We decided not to implement compound terms (arithmetic expressions) for now. The definition for compound term can
# be found below under the definition of "Term".

# Definitions:
# Number:           Signed integers (no positive sign). Float with a dot between two digits. Scientific notation
#                   is supported as aEb where a = fractional number, b = integer which may start with + or -.
# Constant:         A number, any sequence of alphanumerics including underscore but starting with lowercase letter,
#                   or any sequence of characters delimited by single quotes.
# Variable:         Starts with uppercase or underscore, made of alphanumeric characters
# Unknown:          Null values represented with "null" for normal users or "'$NULL'(ID)" for development purposes,
#                   where ID is an integer.
# Term:             Noncompound: variables or constants
#                   Compound: Form of t(t1,...,tn) where t is the functor (which follows the syntax of a noncompound
#                   term) and tn are noncompound terms. In the context of YADI, it refers to arithmetic expressions.
# Predicate symbol: Defined as a sequence of alphanumerics characters + underscore that start with lowercase or
#                   underscore. On a(t1,t2), "a" stands for the predicate symbol. Relation is a synonym of predicate.
# Atom:             Has the form of a(t1, t2) for ti (0<=1<=n). If i = 0, then it is simply written as "a."
# Condition:        Boolean expression containing comparison operators, constants and variables.
# Literal:          A literal can be:
#                   -Positive (an atom).
#                   -Negative. not(body) where body is a body. Used to express the negation of a relation.
# Relation func.:   Built-in functions of the form f(a1,...,an) where ai is a relation (predicate). Built-in
#                   functions implemented are:
#                   -not(a)
#                   -lj(a1,a2,a3) is left outer join where a1 = left relation, a2 = right relation, a3 = join condition.
#                    Same is applicable for rj(a1,a2,a3) for right outer join, and fj(a1,a2,a3) for full outer join.
#                   Outer join functions can be nested.
# Head:             A positive atom that is not a built-in predicate symbol.
# Body:             Comma separated sequence of literals, which may contain built in functions, disjunctions and
#                   division.
# Rule:             head :- body, or just head (called a fact).

class SyntaxException(Exception):
    pass

class parser:
    def __init__(self):
        pass

    def parsesentence(self, sentence):
        #Reserved words
        reserved_null = Literal("is_null") | Literal("is_not_null")
        reserved_is = Literal("is")
        reserved_arith = Literal("sqrt") | Literal("log") | Literal("sin") | Literal("cos") | Literal("tan") | Literal(
            "atan") | Literal("abs") | Literal("float_integer_part") | Literal("float_fractional_part") | Literal(
            "float") | Literal("sign") | Literal("truncate") | Literal("round") | Literal("floor") | Literal("ceiling")
        reserved_not = Literal("not")
        reserved_join = Literal("lj") | Literal("rj") | Literal("fj")
        reserved_aggregates = Literal("count") | Literal("sum") | Literal("avg") | Literal("min") | Literal("max")
        reserved_group = Literal("group_by")
        reserved_duplicates = Literal("distinct")
        reserved_top = Literal("top")
        reserved_answer = Literal("answer")
        reserved_word = reserved_null | reserved_is | reserved_arith | reserved_not | reserved_join | \
                        reserved_aggregates | reserved_group | reserved_duplicates | reserved_top | reserved_answer

        #Special characters
        underscore = Word("_", max=1)                   # Only a single underscore can be used for anon. var
        comma = Literal(",").suppress()                 # Not interested in commas, delete from tokens
        separator = Literal(":-")
        dot = Literal(".").suppress()

        #Comparison operators
        greater = Literal(">")
        less = Literal("<")
        equal = Literal("=")
        g_equal = Literal(">=")
        l_equal = Literal("<=")
        comp_op = g_equal | l_equal | equal | greater | less

        #Number
        number = Combine(Word('-' + nums, nums) + Optional(Literal('.') + Word(nums)) +
                         Optional(Literal('E') + Optional(Word("-+", max=1)) + Word(nums))).setName("number")

        #Constant
        constant = (number | Combine(Word(srange('[a-z]'), alphanums + "_")) |
                    QuotedString("'", unquoteResults=False)).setName("constant")

        #Variable
        variable = (Combine(Optional("_") + Word(srange('[A-Z]')) + Optional(Word(alphanums))) |
                    Combine(Literal("_") + Word(srange('[a-z]'))) |
                    underscore).setName("variable")

        #Unknown
        unknown = (Literal("null") | Combine((Literal("'$NULL'(") + Word(nums) + Literal(")")))).setName("unknown")

        #Terms
        noncompound = (variable | constant).setName("noncompound")
        term = noncompound

        #Atom
        predicate_symbol = Combine((Optional(Literal('_')) + Word(srange('[a-z]')) + Optional(Word(alphanums + '_'))) |
                                   (OneOrMore(Literal('_')) + Word(alphanums, min=1) + Optional(
                                       Word(alphanums + '_')))).setName("predicate_symbol")

        atom = ((predicate_symbol + Literal("(").suppress() + Group(term + Optional(OneOrMore(comma | term))) +
                 Literal(")").suppress()) | predicate_symbol).setName("atom")

        #Comparison and conditions
        comparison = Group(noncompound + comp_op + noncompound).setName("comparison")

        #Literals
        conj_disj_div = Literal(",").suppress() | Literal(";") | Literal("division")
        positive = Group(atom).setName("positive_atom")
        literal = positive.setName("literal")

        #Relation functions
        not_function = Group(Literal("not") + Literal("(").suppress() + positive + Literal(")").suppress()).setName(
            "not_function")
        join_types = (Literal("lj") | Literal("rj") | Literal("fj")).setName("join_type")
        join_base = (join_types + Literal('(').suppress() + Group(atom) + comma + Group(
            atom) + comma + comparison + Literal(')').suppress()).setName("join_base")
        relation_function = (not_function | join_base).setName("relation_function")

        #Rules and facts
        head = NotAny(reserved_word) + positive.setName("head")
        body_part = relation_function | comparison | literal
        body = (body_part + ZeroOrMore(conj_disj_div + body_part)).setName("body")
        temporary_view = body
        rule = (OneOrMore(Group(((head + separator + body) | temporary_view | head) + dot)) + StringEnd()).setName(
            "expression").setFailAction(self.syntax)

        test = rule.parseString(sentence)
        return test

    def syntax(self, s, loc, expr, err):
        x = "Syntax error on string {0!r}, loc {1!r} of '{2!r}'. Details: {3!r}".format(s, loc, expr, err)
        raise SyntaxException(x)