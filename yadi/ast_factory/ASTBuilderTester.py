
from .ASTBuilder import ASTBuilder
from ..dataStructures.constraint import Constraint
from ..dataStructures.element import Variable, Constant, Wildcard
from ..dataStructures.query import ConjunctiveQuery
from ..dataStructures.relation import RelationInQuery

__author__ = 'caioseguin'

# Function that compares the ASTFactory output with an expected input.
# It compares the two using the str() method.
# Unfortunately, it does not implement a type matching check.

def hardCodedTest():
    ast_builder = ASTBuilder()

    input_list = []
    expected_answer_list = []
    result_list = []

    # q(X,Y):- s(X)

    input = ([[['q', ['X', 'Y']], ':-', ['s', ['X']]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False)], [],
                                       RelationInQuery('q', [Variable('X'), Variable('Y')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X)

    input = ([[['q', ['X']], ':-', ['s', ['X']]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False)], [],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X), not t(U)

    input = ([[['q', ['X']], ':-', ['s', ['X']], ['not', ['t', ['U']]]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False),
                                        RelationInQuery('t', [Variable('U')], True)], [],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X,U), not t(U)

    input = ([[['q', ['X']], ':-', ['s', ['X', 'U']], ['not', ['t', ['U']]]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X'), Variable('U')], False),
                                        RelationInQuery('t', [Variable('U')], True)], [],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X), not t(U), U = 2

    input = ([[['q', ['X']], ':-', ['s', ['X']], ['not', ['t', ['U']]], ['U', '=', '2']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False),
                                        RelationInQuery('t', [Variable('U')], True)],
                                       [Constraint(Variable('U'), Constant('2'), '=')],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X), not t(U), u < 2

    input = ([[['q', ['X']], ':-', ['s', ['X']], ['not', ['t', ['U']]], ['U', '<', '2']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False),
                                        RelationInQuery('t', [Variable('U')], True)],
                                       [Constraint(Variable('U'), Constant('2'), '<')],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X), not t(U), U = X

    input = ([[['q', ['X']], ':-', ['s', ['X']], ['not', ['t', ['U']]], ['U', '=', 'X']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False),
                                        RelationInQuery('t', [Variable('U')], True)],
                                       [Constraint(Variable('U'), Variable('X'), '=')],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X,Y):- s(X,Y), y < 3

    input = ([[['q', ['X', 'Y']], ':-', ['s', ['X', 'Y']], ['Y', '<', '3']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X'), Variable('Y')], False)],
                                       [Constraint(Variable('Y'), Variable('3'), '<')],
                                       RelationInQuery('q', [Variable('X'), Variable('Y')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X), not t(Y), X = Y

    input = ([[['q', ['X']], ':-', ['s', ['X']], ['not', ['t', ['Y']]], ['X', '=', 'Y']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False),
                                        RelationInQuery('t', [Variable('Y')], True)],
                                       [Constraint(Variable('X'), Variable('Y'), '=')],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X,Z):- s(X,Y), not t(A,Z), Z = Y

    input = ([[['q', ['X', 'Z']], ':-', ['s', ['X', 'Y']], ['not', ['t', ['A', 'Z']]], ['Z', '=', 'Y']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X'), Variable('Y')], False),
                                        RelationInQuery('t', [Variable('A'), Variable('Z')], True)],
                                       [Constraint(Variable('Z'), Variable('Y'), '=')],
                                       RelationInQuery('q', [Variable('X'), Variable('Z')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X):- s(X, Y, Z), Y = 2, Z = Y

    input = ([[['q', ['X']], ':-', ['s', ['X', 'Y', 'Z']], ['Y', '=', '2'], ['Z', '=', 'Y']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X'), Variable('Y'), Variable('Z')], False)],
                                       [Constraint(Variable('Y'), Constant('2'), '='),
                                        Constraint(Variable('Z'), Variable('Y'), '=')],
                                       RelationInQuery('q', [Variable('X')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # r(X,'Nantes') :- r(X)

    input = ([[['r', ['X', "'Nantes'"]], ':-', ['r', ['X']]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('r', [Variable('X')], False)],[],
                                       RelationInQuery('r', [Variable('X'), Constant("'Nantes'")]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # r(X,Y,Z,_,2) :- s(X), Y=X, X=2

    input = ([[['r', ['X', 'Y', 'Z', '_', '2']], ':-', ['s', ['X']], ['Y', '=', 'X'], ['X', '=', '2']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X')], False)],
                                       [Constraint(Variable('Y'), Variable('X'), '='),
                                        Constraint(Variable('X'), Variable('2'), '=')],
                                       RelationInQuery('r', [Variable('X'), Variable('Y'), Variable('Z'),
                                                             Wildcard(), Constant('2')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # q(X,Y) :- s(_,Y), t(X,_), u(_), v(_,_)

    input = ([[['q', ['X', 'Y']], ':-', ['s', ['_', 'Y']], ['t', ['X', '_']], ['u', ['_']], ['v', ['_', '_']]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Wildcard(),Variable('Y')], False),
                                        RelationInQuery('t', [Variable('X'), Wildcard()], False),
                                        RelationInQuery('u', [Wildcard()], False),
                                        RelationInQuery('v', [Wildcard(),Wildcard()], False)],[],
                                       RelationInQuery('q', [Variable('X'), Variable('Y')]))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # answer(X,Y):-S(X,Z),S(Y,Z),X>Y

    input = ([[['answer', ['X', 'Y']], ':-', ['s', ['X', 'Z']], ['s', ['Y', 'Z']], ['X', '>', 'Y']]])
    expected_answer = ConjunctiveQuery([RelationInQuery('s', [Variable('X'),Variable('Z')],False),
                                        RelationInQuery('s', [Variable('Y'),Variable('Z')],False)],
                                       [Constraint(Variable('X'), Variable('Y'),'>')],
                                       RelationInQuery('answer', [Variable('X'),Variable('Y')], False))
    output = ast_builder.buildAST(input)[0]
    input_list.append(input)
    expected_answer_list.append(expected_answer)
    result_list.append(checkAnswer(output, expected_answer))

    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #
    # ---------------------------------------------------------------------------------------------------------------- #

    failed_test_list = []

    for i in range(0, len(result_list)):
        result = result_list[i]
        if not result:
            failed_test_list.append(i+1)

    test_score = str(len(result_list) - len(failed_test_list)) + '/' + str(len(result_list))

    print('*** Test Results ***', '\n',
          '*** Score: ', test_score, '\n',
          #'*** Inputs: ', '\n',
          #input_list, '\n',
          #"\n".join(item[0] for item in input_list), '\n',
          #'*** Expected answers: ', '\n',
          #expected_answer_list, '\n'
          #"\n".join(item[0] for item in expected_answer_list), '\n',
          '*** Failed tests: ', failed_test_list)


def checkAnswer(answer_1, answer_2):
    return str(answer_1) == str(answer_2)

def main():
    hardCodedTest()

main()
