/* FOL Statements as Prolog clauses */

/* facts */
female(princess_ann).
queen(queen_elizabeth).
female(queen_elizabeth).
male(prince_andrew).
male(prince_edward).
male(prince_charles).

/* relationships */
older(prince_andrew, prince_edward).
older(prince_charles, princess_ann).
older(princess_ann, prince_andrew).

offspring(prince_edward, queen_elizabeth).
offspring(princess_ann, queen_elizabeth).
offspring(prince_andrew, queen_elizabeth).
offspring(prince_charles, queen_elizabeth).


/* Throne Succession Rule */

/* Older child > Younger Child */
precedes(X, Y):-	 
	not(queen(X)), not(queen(Y)),
	is_older(X, Y),
	offspring(X, A), offspring(Y, A).


/* Succession Order Sorting Algorithm */
succession_list_sort([A|B], SortedList):- 
	succession_list_sort(B, Sorted_Tail), insert(A, Sorted_Tail, SortedList).
succession_list_sort([], []).

insert(A, [B|C], [B|D]):- 
	not(precedes(A,B)), !, insert(A, C, D).
insert(A, C, [A|C]).


/* Return succession list */
/* Sorted in order of succession ordering */
sortedSuccessionList(X, SuccessionList):-
	findall(Y, offspring(Y,X), Offspring), succession_list_sort(Offspring, SuccessionList).


/* Helper Functions */
is_older(A, B):-
	older(A, B).
is_older(A, B):-
	older(A, X), is_older(X, B).