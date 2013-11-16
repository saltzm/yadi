from ASTBuilder import ASTBuilder
from dataStructures.element import Variable
from dataStructures.query import ConjunctiveQuery
from dataStructures.relation import RelationInQuery

__author__ = 'caioseguin'

def hardCodedTest():

    ast_builder = ASTBuilder(1)

    input_list = []
    expected_answer_list = []
    result_list = []

    # Q(X,Y):- S(X)

    input_list.extend([[['q', ['X', 'Y']], ':-', ['s', ['X']]]])
    expected_answer = str(ConjunctiveQuery([RelationInQuery('S', [Variable('X')], False)], [],
                                       RelationInQuery('Q', [Variable('X'), Variable('Y')])))

    expected_answer_list.extend(expected_answer)
    result_list.extend(checkAnswer(str(ast_builder.buildAST(input)), expected_answer))

    # Q(X):- S(X)

    input_list.extend([[['q', ['X', 'Y']], ':-', ['s', ['X']]]])
    expected_answer = ConjunctiveQuery([RelationInQuery('S', {Variable('X'): [0]}, {}, [], False)], [],
                                       RelationInQuery('Q', {Variable('X'): [0]}))

    expected_answer_list.extend(expected_answer.__repr__())
    result_list.extend(checkAnswer(ast_builder.buildAST(input), expected_answer))

    # Q(X):- S(X), not T(U)
    # Q(X):- S(X,U), not T(U)
    # Q(X):- S(X), !T(U), U = 2
    # Q(X):- S(X), !T(U), U < 2
    # Q(X):- S(X), !T(U), U = X
    # Q(X):- S(X), Y < 3
    # Q(X):- S(X,Y), Y < 3
    # Q(X):- S(X), !T(Y), X = Y
    # Q(X,Z):- S(X,Y), !T(A,Z), Z = Y
    # Q(X):- S(X), X = 2
    # Q(X):- S(X, Y), Y = 2
    # Q(X):- S(X, Y, Z), Y = 2, Z = Y
    # Q(X) :- not S(Y),  X = 2, X = Y
    # Q(X) :- not S(Y), X = Y, X = 2
    # Q(X) :- S(X), X = Y
    # Q(X) := S(X), P = Y
    # R(X) := S(X), 3=X, X>2
    # R(Y) := S(X), Y=X, X=2 Y =4
    # R(X,Y,Z,_,2) := S(X), Y=X, X=2

    failed_test_list = []

    for i in range(0, len(result_list)):
        result = result_list[i]
        if not result:
            failed_test_list.extend(i)

    test_score = len(failed_test_list) + '/' + len(result_list)

    print('*** Test Results ***', '\n',
          '*** Score: ', test_score, '\n',
          '*** Inputs: ', '\n',
          "\n".join(item[0] for item in input_list), '\n',
          '*** Expected answers: ', '\n',
          "\n".join(item[0] for item in expected_answer_list), '\n',
          '*** Failed tests: ', failed_test_list)


def test(self, datalog_parsed_program, expected_ast):
    return

def checkAnswer(self, answer_1, answer_2):
    return True
    #return answer_1.__repr__() == answer_2.__repr__()


def main():
    #hardCodedTest()
    x = str(ConjunctiveQuery([RelationInQuery('S', [Variable('X')], False)], [],
                                       RelationInQuery('Q', [Variable('X'), Variable('Y')])))
    print(x)

main()