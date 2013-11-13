from Parser import *

p = Parser()

p.parsesentence("q")                                    # Atom, zero arity
p.parsesentence("q(x)")                                 # Atom, one var
p.parsesentence("q('3')")                               # Atom, string
p.parsesentence("q(x,y)")                               # Atom, two-arity
p.parsesentence("q(_,x)")                               # Atom, anonymous variable
p.parsesentence("_ab(a)")                               # Predicate symbol with underscore
p.parsesentence("q2(x,z,b,'a')")                        # Predicate symbol with number
p.parsesentence("__ab_55(a,b,c)")                       # Predicate symbol with number and underscore
p.parsesentence("q(x,y) :- k(x,y)")                     # Rule with one literal
p.parsesentence("q(x,y) :- k(x,h), _v3(n,k)")           # Rule with two literals
p.parsesentence("q(x,y) :- a;b")                        # Rule with disjunction of two zero-arity atoms
p.parsesentence("q(x,y) :- a(x);b(x)")                  # Rule with disjunction of two 1-arity atoms
p.parsesentence("q(x,y) :- a division b")               # Rule with division of two zero-arity atoms
p.parsesentence("q(x,y) :- a(x,y) division b(x,y)")     # Rule with division of two two-arity atoms
p.parsesentence("q(x,y,z) :- a(x),a;b")                 # Rule with one-arity atom, disjunction of two zero-arity atoms
p.parsesentence("q(x,y) :- a(x), t>5")                  # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), t<5")                  # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), t>=5")                 # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), t<=5")                 # Rule with one-arity atom, boolean comparison
p.parsesentence("q(x,y) :- a(x), gd=5")                 # Rule with one-arity atom, boolean comparison