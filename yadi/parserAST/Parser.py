from pyparsing import *

# TODO: 1. Rename variables to match definitions below.
# TODO: 2. Allow underscore use in constants inside terms.
# TODO: 3. Implement string use for constants and predicate symbols.
# TODO: 4. Implement comment parsing.
# TODO: 5. Implement disjunctions.
# TODO: 6. Implement use of variables in term list.
# TODO: 7. Implement semicolon.

# Definitions:
# Literal:          predicate symbol followed by an optional parenthesized list of comma separated terms.
#                   Ex: parent(a,b)
# Predicate symbol: identifier or string
# Term:             variable or constant
# Constant:         identifier or string
# Variable:         sequence of Latin capital and small letters, digits, and the underscore character.
#                   A variable must begin with a Latin capital letter.
# Identifier:       a sequence of printing characters that does not contain any of the following characters:
#                   ‘(’, ‘,’, ‘)’, ‘=’, ‘:’, ‘.’, ‘~’, ‘?’, ‘"’, ‘%’, space. An identifier must not begin with a Latin
#                   capital letter. Note that the characters that start punctuation are forbidden in identifiers, but
#                   the hyphen character is allowed. --> NEED TO IMPLEMENT THIS COMPLETELY <--

class Parser:
    def __init__(self): pass

    def parseSentence(self, sentence):
        #Character sets
        dot = Literal(".").suppress()
        comma = Literal(",").suppress()                 # Not interested in commas, delete from tokens
        underscore = Word("_", max=1)                   # Only a single underscore can be used for anon. var
        numbers = Word("0123456789")
        letters = Word("abcdefghijklmnopqrstuwxyz")
        clauseVar = Combine(Word("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + Optional(Word(alphanums)))  # Node name
        
        #Parenthesis
        lParen = Literal("(").suppress()                # Not interested in parenthesis, delete from tokens
        rParen = Literal(")").suppress()                # Not interested in parenthesis, delete from tokens

        #Comparison operators
        greater = Literal(">")
        less = Literal("<")
        equal = Literal("=")
        gEqual = Literal(">=")
        lEqual = Literal("<=")
        compOp = greater | less | equal | gEqual | lEqual 

        #Operators
        separator = Literal(":-")
        andString = Literal("and").suppress()
        andOps = andString | comma
        negation = Literal("¬")

        #Valid variable format examples: "x, xyz, x1, x123, _"
        variables = underscore | Combine(letters + numbers) | letters

        #Comparisons
        comparison = (letters | Combine(letters + numbers)) + compOp + numbers

        #Head expression
        node = Optional(negation) + clauseVar + lParen + Group(variables + ZeroOrMore(comma + variables)) + rParen

        #body expression
        body = Group(node) + ZeroOrMore(andOps + Group(node)) + ZeroOrMore(andOps + Group(comparison)) + dot

        #Complete expression
        expr = OneOrMore(Group(Group(node) + separator + body) | Group(node + dot)) + StringEnd()

        try:
            test = expr.parseString(sentence)
            print(test)
        except ParseException as pe:
            print(pe)