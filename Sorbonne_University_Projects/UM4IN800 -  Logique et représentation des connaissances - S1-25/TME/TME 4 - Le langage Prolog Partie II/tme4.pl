/*
Yuxiang ZHANG 21202829
Kenan Alsafadi 21502362
*/

/* 
Exercice 1

?- [a, [b, c], d] = [X]. 
    false.

?- [a, [b, c], d] = [X, Y, Z]. 
    X = a,
    Y = [b, c],
    Z = d.

?- [a, [b, c], d] = [a | L].
    L = [[b, c], d].

?- [a, [b, c], d] = [X, Y]. 
    false.

?- [a, [b, c], d] = [X | Y].
    X = a,
    Y = [[b, c], d].

?- [a, [b, c], d] = [a, b | L].
    false.

?- [a, b, [c, d]] = [a, b | L].
    L = [[c, d]].

?- [a, b, c, d | L1] = [a, b | L2].
    L2 = [c, d|L1].
*/

/*
Exercice 2

Question 2.1
*/

concatene([], L, L).
concatene([X | L1], L2, [X | L3]) :-
    concatene(L1, L2, L3).

/* Test
?- concatene([a, b, c], [d, e], L3).
    L3 = [a, b, c, d, e].

?- concatene(L1, [d, e], [a, b, c, d, e]).
    L1 = [a, b, c] ;
    false.

?- concatene([a,b],X,[a,b,c,d]).
    X = [c, d].

?- concatene([X], L, [a, b, c, d]).
    X = a,
    L = [b, c, d].

?- concatene(L, [X], [a, b, c, d]).
    L = [a, b, c],
    X = d ;
    false.

?- concatene(L1, L2, [a, b, c]).
    L1 = [],
    L2 = [a, b, c] ;
    L1 = [a],
    L2 = [b, c] ;
    L1 = [a, b],
    L2 = [c] ;
    L1 = [a, b, c],
    L2 = [] ;
    false.
*/

/*
Question 2.2
*/

inverse([], []).
inverse([X | L], Res) :-
    inverse(L, Ltmp),
    concatene(Ltmp, [X], Res).

/*
?- inverse(L, [a, b, c]).
    L = [c, b, a] ;
Appel récursif non terminale.

?- inverse([a,b,c], [c,b,a]). 
    true.

?- inverse([a,b,c],Res).
    Res = [c, b, a].
*/

/*
Question 2.3
*/

supprime([], _, []).

supprime([Y|T], Y, R) :-
    supprime(T, Y, R).

supprime([H|T], Y, [H|R]) :-
    H \== Y,
    supprime(T, Y, R).

/*
Quand 'H \= Y'
?- supprime([1, 2, 3, 1], 1, Res).
    Res = [2, 3] ;

?- supprime([1, 2, 3, 1], X, [2, 3]).
    X = 1 ;

?- supprime([1, 2, 3], Y, [1, 2, 3]).
    false.

?- supprime([1, 2, 3, 1], X, [1, 3, 1]).
    false.
*/

/*
Quand 'H \== Y'
?- supprime([1, 2, 3, 1], 1, Res).
    Res = [2, 3] ;

?- supprime([1, 2, 3, 1], X, [2, 3]).
    X = 1 ;

?- supprime([1, 2, 3], Y, [1, 2, 3]).
    true.

?- supprime([1, 2, 3, 1], X, [1, 3, 1]).
    X = 2 ;
    false.
*/

/*
Question 2.4
*/

filtre(L1, [], L1).
filtre(L1, [X | L], L3) :-
    supprime(L1, X, Tmp),
    filtre(Tmp, L, L3).

/*
?- filtre([1,2,3,4,3,4,2,1], [2,4], L).
    L = [1, 3, 3, 1] ;
    false.

?- filtre([a,b,c,a,b], [a], X).
    X = [b, c, b] ;
    false.

?- filtre([1,2,3], F, [1,3]).
    ERROR: Stack limit (1.0Gb) exceeded
    ERROR:   Stack sizes: local: 2Kb, global: 1.0Gb, trail: 0Kb
    ERROR:   Stack depth: 38,017,330, last-call: 100%, Choice points: 7
    ERROR:   In:
    ERROR:     [38,017,330] user:filtre([], [length:1|_228104156], [length:2])
    ERROR:     [14] user:filtre('<garbage_collected>', '<garbage_collected>', [length:2])
    ERROR:     [13] user:filtre('<garbage_collected>', '<garbage_collected>', [length:2])
    ERROR:     [12] user:filtre('<garbage_collected>', '<garbage_collected>', [length:2])
    ERROR:     [11] '$toplevel':toplevel_call('<garbage_collected>')
    ERROR: 
    ERROR: Use the --stack_limit=size[KMG] command line option or
    ERROR: ?- set_prolog_flag(stack_limit, 2_147_483_648). to double the limit.
*/

/*
Exercice 3
*/

/*
Question 3.1
*/

palindrome([]).
palindrome([_]).
palindrome(L1) :-
    inverse(L1, L1).

/*
?- palindrome([l,a,v,a,l]).
    true.

?- palindrome([n,a,v,a,l]).
    false.
*/
    
/*
Question 3.2
*/

palindrome2([]).          
palindrome2([_]).         
palindrome2(L) :-
    concatene([X|Middle], [X], L),   
    palindrome2(Middle).

/*
?- palindrome2([l,a,v,a,l]).
    true 

?- palindrome2([n,a,v,a,l]).
    false.
*/