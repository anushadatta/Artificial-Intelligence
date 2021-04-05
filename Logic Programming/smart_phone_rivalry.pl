/* FOL Statements as Prolog clauses */

/* facts */
company(sumsum).
company(appy).
smartphonetechnology(galactica-s3).

/* relationships */
competitors(sumsum, appy).
develop(sumsum, galactica-s3).
boss(stevey, appy).
steal(stevey, galactica-s3).

/* defining conjunctive/disjunctive sentences */
business(X):-
	smartphonetechnology(X).

competitors(X, Y):-
	competitors(Y, X).

rivals(X, Y):-
	competitors(X, Y).

unethical(A):-
	boss(A, B), steal(A, D), rivals(B, C), company(C), develop(C, D), business(D).
