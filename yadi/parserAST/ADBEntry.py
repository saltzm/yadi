from Parser import parser

p = parser()

#Tests to check syntax
p.parsesentence("q(x,y) :- a(x), b(x);c(x), d(x); e(x).")
p.parsesentence("q.")                                    # Atom, zero arity
p.parsesentence("q(x).")                                 # Atom, one var
p.parsesentence("q('3').")                               # Atom, string
p.parsesentence("q(x,y).")                               # Atom, two-arity
p.parsesentence("q(_,x).")                               # Atom, anonymous variable
p.parsesentence("_ab(a).")                               # Predicate symbol with underscore
p.parsesentence("q2(x,z,b,'a').")                        # Predicate symbol with number
p.parsesentence("__ab_55(a,b,c).")                       # Predicate symbol with number and underscore
p.parsesentence("q(x,y) :- k(x,y).")                     # Rule with one literal
p.parsesentence("q(x,y) :- a(foo_foo).")                 # Rule with one literal using constant
p.parsesentence("q(x,y) :- k(_ab).")                     # Rule with one literal with constant starting with underscore
p.parsesentence("q(x,y) :- k(X).")                       # Rule with one literal with one variable
p.parsesentence("q(x,y) :- k(x,h), _v3(n,k).")           # Rule with two literals
p.parsesentence("q(x,y) :- a;b.")                        # Rule with disjunction of two zero-arity atoms
p.parsesentence("q(x,y) :- a(x);b(x).")                  # Rule with disjunction of two 1-arity atoms
p.parsesentence("q(x,y) :- a division b.")               # Rule with division of two zero-arity atoms
p.parsesentence("q(x,y) :- a(x,y) division b(x,y).")     # Rule with division of two two-arity atoms
p.parsesentence("q(x,y,z) :- a(x),a;b.")                 # Rule with one-arity atom, disjunction of two zero-arity atoms
p.parsesentence("q(x,y) :- a(x), t>5.")                  # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), t<5.")                  # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), t>=5.")                 # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), t<=5.")                 # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), gd=5.")                 # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y,z) :- a(x), t=4.0.")              # Rule with one-arity atom, comparison using float
p.parsesentence("q(x,y,z) :- a(x), t=4.0E6.")            # Rule with one-arity atom, comparison using float+E
p.parsesentence("q(x,y,z) :- a(x), t=4.0E+6.")           # Rule with one-arity atom, comparison using float+E+'+'
p.parsesentence("q(x,y,z) :- a(x), t=4.0E-6.")           # Rule with one-arity atom, comparison using float+E+'-'
p.parsesentence("q(x,y,z) :- a(x), t=4.0, k(x).")        # Rule with one-arity atom, comparison, atom
p.parsesentence("q(x) :- x(g), not(a(x,y)).")            # Rule with one-arity atom, negation
p.parsesentence("q(x,y). k(x).")                         # Two facts in a line.
p.parsesentence("q(x,y). q(x,y) :- a(b,c).")             # A fact and a rule in a line.
p.parsesentence("q(x,y). q(x,y) :- a(b,c). a(b).")       # A fact, a rule and a fact in a line.
p.parsesentence("q(x,y) :- a(b), X=3; Y>5.")             # Rule with one-arity atom, disjunctive comparison.
p.parsesentence("q(x,y) :- a(b), X=3, Y>5.")             # Rule with one-arity atom, conjunctive comparison.
p.parsesentence("q(x,y) :- a(b), X=3, Y>5, X=3; Y>5.")   # Rule with one-arity atom, two two-term comparisons.
p.parsesentence("r(X) :- not(t(Y)), X = Y, s(Y).")       # Rule with a negation in front.
p.parsesentence("r(x) :- r(a,X); not(q(X,b)), lj(a,b,x).")      # Rule with a left join
p.parsesentence("q(X,Z) :- s(X,Y), not(t(X)), Y=Z.")
p.parsesentence("q(X,Z) :- t>5, s(X,Y), not(t(X)), Y=Z.")
p.parsesentence("q(X,Y):- s(X).\nq(X,Y):- s(Y).")        # Two statements broken down in two lines.
p.parsesentence("q(x,y) :- a(b), X=3, 3>Y, X=3; 5>X.")   # Rule with one-arity atom, two two-term comparisons.

#Incorporation of all elements
p.parsesentence("_a45(x,Y,_343,'a') :- __x_43A(k,3.5E+3,x), A>=4; t=5, a(q,x);r(x,Y), a division y. q(x,y).")

#Rules (that actually make sense)
p.parsesentence("q(X,Y):- s(X).")
p.parsesentence("q(X):- s(X).")
p.parsesentence("q(X):- s(X), not(t(U)).")
p.parsesentence("q(X):- s(X,U), not(t(U)).")
p.parsesentence("q(X):- s(X), not(t(U)), U = 2.")
p.parsesentence("q(X):- s(X), not(t(U)), U < 2.")
p.parsesentence("q(X):- s(X), not(t(U)), U = X.")
p.parsesentence("q(X):- s(X), Y < 3.")
p.parsesentence("q(X):- s(X,Y), Y < 3.")
p.parsesentence("q(X):- s(X), not(t(Y)), X = Y.")
p.parsesentence("q(X,Z):- s(X,Y), not(t(A,Z)), Z = Y.")
p.parsesentence("q(X):- s(X), X = 2.")
p.parsesentence("q(X):- s(X, Y), Y = 2.")
p.parsesentence("q(X):- s(X, Y, Z), Y = 2, Z = Y.")
p.parsesentence("q(X) :- not(s(Y)),  X = 2, X = Y.")
p.parsesentence("q(X) :- not(s(Y)), X = Y, X = 2.")
p.parsesentence("q(X) :- s(X), X = Y.")
p.parsesentence("q(X) :- s(X), P = Y.")
p.parsesentence("r(X) :- s(X), 3=X, X>2.")
p.parsesentence("r(Y) :- s(X), Y=X, X=2, Y =4.")
p.parsesentence("r(X,Y,Z,_,2) :- s(X), Y=X, X=2.")
p.parsesentence("q(X,Y) :- s(_,Y), t(X,_), u(_), v(_,_).")
p.parsesentence("q(X,Y), s(x) :- s(_,Y), t(X,_), u(_), v(_,_).")