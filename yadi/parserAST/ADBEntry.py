from .Parser import parser

p = parser()

#Tests to check syntax
print(p.parsesentence("q."))                                    # Atom, zero arity
print(p.parsesentence("q(x)."))                                 # Atom, one var
print(p.parsesentence("q('3')."))                               # Atom, string
print(p.parsesentence("q(x,y)."))                               # Atom, two-arity
print(p.parsesentence("q(_,x)."))                               # Atom, anonymous variable
print(p.parsesentence("_ab(a)."))                               # Predicate symbol with underscore
print(p.parsesentence("q2(x,z,b,'a')."))                        # Predicate symbol with number
print(p.parsesentence("__ab_55(a,b,c)."))                       # Predicate symbol with number and underscore
print(p.parsesentence("q(x,y) :- k(x,y)."))                     # Rule with one literal
print(p.parsesentence("q(x,y) :- a(foo_foo)."))                 # Rule with one literal using constant
print(p.parsesentence("q(x,y) :- k(_ab)."))                     # Rule with one literal with constant starting with underscore
print(p.parsesentence("q(x,y) :- k(X)."))                       # Rule with one literal with one variable
print(p.parsesentence("q(x,y) :- k(x,h), _v3(n,k)."))           # Rule with two literals
print(p.parsesentence("q(x,y) :- a;b."))                        # Rule with disjunction of two zero-arity atoms
print(p.parsesentence("q(x,y) :- a(x);b(x)."))                  # Rule with disjunction of two 1-arity atoms
print(p.parsesentence("q(x,y) :- a division b."))               # Rule with division of two zero-arity atoms
print(p.parsesentence("q(x,y) :- a(x,y) division b(x,y)."))     # Rule with division of two two-arity atoms
print(p.parsesentence("q(x,y,z) :- a(x),a;b."))                 # Rule with one-arity atom, disjunction of two zero-arity atoms
print(p.parsesentence("q(x,y) :- a(x), t>5."))                  # Rule with one-arity atom, boolean comparison
print(p.parsesentence("q(x,y) :- a(x), t<5."))                  # Rule with one-arity atom, boolean comparison
print(p.parsesentence("q(x,y) :- a(x), t>=5."))                 # Rule with one-arity atom, boolean comparison
print(p.parsesentence("q(x,y) :- a(x), t<=5."))                 # Rule with one-arity atom, boolean comparison
print(p.parsesentence("q(x,y) :- a(x), gd=5."))                 # Rule with one-arity atom, boolean comparison
print(p.parsesentence("q(x,y,z) :- a(x), t=4.0."))              # Rule with one-arity atom, comparison using float
print(p.parsesentence("q(x,y,z) :- a(x), t=4.0E6."))            # Rule with one-arity atom, comparison using float+E
print(p.parsesentence("q(x,y,z) :- a(x), t=4.0E+6."))           # Rule with one-arity atom, comparison using float+E+'+'
print(p.parsesentence("q(x,y,z) :- a(x), t=4.0E-6."))           # Rule with one-arity atom, comparison using float+E+'-'
print(p.parsesentence("q(x,y,z) :- a(x), t=4.0, k(x)."))        # Rule with one-arity atom, comparison, atom
print(p.parsesentence("q(x) :- x(g), not(a(x,y))."))            # Rule with one-arity atom, negation
print(p.parsesentence("q(x,y). k(x)."))                         # Two facts in a line.
print(p.parsesentence("q(x,y). q(x,y) :- a(b,c)."))             # A fact and a rule in a line.
print(p.parsesentence("q(x,y). q(x,y) :- a(b,c). a(b)."))       # A fact, a rule and a fact in a line.
print(p.parsesentence("q(x,y) :- a(b), X=3; Y>5."))             # Rule with one-arity atom, disjunctive comparison.
print(p.parsesentence("q(x,y) :- a(b), X=3, Y>5."))             # Rule with one-arity atom, conjunctive comparison.
print(p.parsesentence("q(x,y) :- a(b), X=3, Y>5, X=3; Y>5."))   # Rule with one-arity atom, two two-term comparisons.
print(p.parsesentence("r(X) :- not(t(Y)), X = Y, s(Y)."))       # Rule with a negation in front.
print(p.parsesentence("r(x) :- r(a,X); not(q(X,b)), lj(a,b,x)."))      # Rule with a left join
print(p.parsesentence("q(X,Z) :- s(X,Y), not(t(X)), Y=Z."))
print(p.parsesentence("q(X,Z) :- t>5, s(X,Y), not(t(X)), Y=Z."))
print(p.parsesentence("q(X,Y):- s(X).\nq(X,Y):- s(Y)."))        # Two statements broken down in two lines.
print(p.parsesentence("q(x,y) :- a(b), X=3, 3>Y, X=3; 5>X."))   # Rule with one-arity atom, two two-term comparisons.
print(p.parsesentence("q(X,Y), s(x)."))                         # Temporary view
print(p.parsesentence("q(X,Y), not(x(t,y))."))                  # Temporary view
print(p.parsesentence("q(X,Y):- s(X).\nq(X,Y):- s(X).\nq(X,Y):- s(X)."))
print(p.parsesentence("q(X,3) :- s(X)."))

#Incorporation of all elements
print(p.parsesentence("_a45(x,Y,_343,'a') :- __x_43A(k,3.5E+3,x), A>=4; t=5, a(q,x);r(x,Y), a division y. q(x,y)."))

#Rules (that actually make sense)
print(p.parsesentence("q(X,Y):- s(X)."))
print(p.parsesentence("q(X):- s(X)."))
print(p.parsesentence("q(X):- s(X), not(t(U))."))
print(p.parsesentence("q(X):- s(X,U), not(t(U))."))
print(p.parsesentence("q(X):- s(X), not(t(U)), U = 2."))
print(p.parsesentence("q(X):- s(X), not(t(U)), U < 2."))
print(p.parsesentence("q(X):- s(X), not(t(U)), U = X."))
print(p.parsesentence("q(X):- s(X), Y < 3."))
print(p.parsesentence("q(X):- s(X,Y), Y < 3."))
print(p.parsesentence("q(X):- s(X), not(t(Y)), X = Y."))
print(p.parsesentence("q(X,Z):- s(X,Y), not(t(A,Z)), Z = Y."))
print(p.parsesentence("q(X):- s(X), X = 2."))
print(p.parsesentence("q(X):- s(X, Y), Y = 2."))
print(p.parsesentence("q(X):- s(X, Y, Z), Y = 2, Z = Y."))
print(p.parsesentence("q(X) :- not(s(Y)),  X = 2, X = Y."))
print(p.parsesentence("q(X) :- not(s(Y)), X = Y, X = 2."))
print(p.parsesentence("q(X) :- s(X), X = Y."))
print(p.parsesentence("q(X) :- s(X), P = Y."))
print(p.parsesentence("r(X) :- s(X), 3=X, X>2."))
print(p.parsesentence("r(Y) :- s(X), Y=X, X=2, Y =4."))
print(p.parsesentence("r(X,Y,Z,_,2) :- s(X), Y=X, X=2."))
print(p.parsesentence("q(X,Y) :- s(_,Y), t(X,_), u(_), v(_,_)."))
print(p.parsesentence("q(x,y)."))
