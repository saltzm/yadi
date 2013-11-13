from pyparsing import *

# TODO: 1. Review safety of strings on constants.
# TODO: 2. Implement nested joins.
# TODO: 3. Negation inside a disjunction or a division is not yet supported. i.e: r(a,X);not(q(X,b))
# TODO: 4. Block negation from occurring in the head. Modify definition of head.

# Notes:
# - We decided not to implement compound terms for now.

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
#                   term) and tn are noncompound terms.
# Predicate symbol: Defined as a sequence of alphanumerics characters + underscore that start with lowercase or
#                   underscore. On a(t1,t2), "a" stands for the predicate symbol. Relation is a synonym of predicate.
# Atom:             Has the form of a(t1, t2) for ti (0<=1<=n). If i = 0, then it is simply written as "a."
# Condition:        Boolean expression containing conjunctions (,/2), disjunctions (;/2), comparison operators,
#                   constants and variables.
# Literal:
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

class Parser:
    def __init__(self):
        pass

    def parsesentence(self, sentence):
        #Special characters
        underscore = Word("_", max=1)                   # Only a single underscore can be used for anon. var
        comma = Literal(",").suppress()                 # Not interested in commas, delete from tokens
        separator = Literal(":-")

        #Comparison operators
        greater = Literal(">")
        less = Literal("<")
        equal = Literal("=")
        gEqual = Literal(">=")
        lEqual = Literal("<=")
        compOp = gEqual | lEqual | equal | greater | less

        #Expressions
        number = Combine(Word('-' + nums, nums) + Optional(Literal('.') + Word(nums)) +
                         Optional(Literal('E') + Optional(Word("-+", max=1)) + Word(nums)))

        constant = (number | Combine(Word(srange('[a-z]'), alphanums + "_")) |
                    QuotedString("'", unquoteResults=False))

        variable = (Combine(Optional("_") + Word(srange('[A-Z]')) + Optional(Word(alphanums))) |
                    Combine(Literal("_") + Word(srange('[a-z]'))) |
                    underscore)

        unknown = (Literal("null") | Combine((Literal("'$NULL'(") + Word(nums) + Literal(")"))))

        noncompound = variable | constant
        #compound = Combine(noncompound + Literal('(') + OneOrMore(noncompound) + Literal(')'))

        term = noncompound

        predicate_symbol = Combine((Optional(Literal('_')) + Word(srange('[a-z]')) + Optional(Word(alphanums + '_'))) |
                                   (OneOrMore(Literal('_')) + Word(alphanums, min=1) + Optional(Word(alphanums + '_'))))

        atom = (predicate_symbol + Literal("(").suppress() + Group(term + Optional(OneOrMore(comma | term))) +
                Literal(")").suppress()) | predicate_symbol

        comparison = Group(noncompound + compOp + noncompound)
        conjunction = Literal("(").suppress() + comparison + Literal(",") + comparison + Literal(")").suppress()
        disjunction = Literal("(").suppress() + comparison + Literal(";") + comparison + Literal(")").suppress()
        condition = conjunction | disjunction | comparison

        positive = Group(atom)
        disjunctive = Group(atom) + Literal(";") + Group(atom)
        divided = Group(atom) + Literal("division") + Group(atom)
        not_function = Literal("not") + Literal("(").suppress() + Group(disjunctive | divided | positive) + Literal(
            ")").suppress()
        literal = Group(not_function) | disjunctive | divided | positive

        join_types = Literal("lj") | Literal("rj") | Literal("fj")
        join_base = join_types + Literal('(').suppress() + Group(atom) + comma + Group(
            atom) + comma + comparison + Literal(')').suppress()

        relation_function = not_function | join_base

        head = positive
        body = literal + ZeroOrMore(Literal(',').suppress()+(condition | literal))
        rule = ((head + separator + body) | head) + StringEnd()

        try:
            test = rule.parseString(sentence)
            print(test)
        except ParseException as pe:
            print(pe)