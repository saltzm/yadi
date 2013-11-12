from Parser import *

p = Parser()

#Tested and valid cases
p.parseSentence("Q(x,x).")
p.parseSentence("Q(x,_).")
p.parseSentence("Q(x1,test).")
p.parseSentence("Q(x,y).")
p.parseSentence("¬Q(x,y).")
p.parseSentence("Q(g,h) :-    K(x,k), t>5.")
p.parseSentence("Q(k,y) :- J(a,b) and K(l,m).")
p.parseSentence("Q(a,b,c,d,e,f,g) :- K(a) and K(b) , K(c).")
p.parseSentence("Q(a,b,c,d,e,f,g) :- K(a) and K(b), K(c), t=44.")
p.parseSentence("Q(a,b,c,d,e,f,g) :- K(a) and K(b), K(c) and t=44.")
p.parseSentence("Q(a,b,c,d,e,f,g) :- K(a) and K(b), K(c), t=44, k=45 and j=30.")
p.parseSentence("Qkkk566(x,y). Affb(g,_). F(k,k). Q(x,y) :- K(l,k). K(k,y).")
p.parseSentence("¬Q(x,y) :- ¬Q(a,b).")

#Tested cases which should (and throw) an error
p.parseSentence("Q")        #Datalog manual says zero arity is allowed, look into this
p.parseSentence("Q()")
p.parseSentence("Q(,).")
p.parseSentence("Q(x,).")
p.parseSentence("Q(x,y)")
p.parseSentence("Q(x,y, )")
p.parseSentence("Q(x,y,z) :- ")
p.parseSentence("Q(x,y) :- Q(")
p.parseSentence("Q(x,y) :- A(b,c)")
p.parseSentence("Q")





