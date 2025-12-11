/*
Yuxiang ZHANG 21202829
Kenan Alsafadi 21502362
*/

/* Exercice 1
r(a,b).
r(f(X),Y) :- p(X,Y).
p(f(X),Y) :- r(X,Y). 
*/

/* Exercice 2
r(a,b).
q(X,X).
q(X,Z) :- r(X,Y),q(Y,Z).
*/

% Exercice 3
% Question 3.1

% Règles
revise(X)    :- serieux(X).            % Les étudiants sérieux révisent leurs examens.
fait_devoirs(X) :- consciencieux(X).   % Un étudiant consciencieux fait ses devoirs pour le lendemain.
reussit(X)   :- revise(X).             % Les étudiants qui révisent réussissent.
serieux(X)   :- fait_devoirs(X).       % Les étudiants qui font leurs devoirs sont sérieux.

% Faits
consciencieux(pascal).
consciencieux(zoe).

/* 
Question 3.2
La requête suivante permet de répondre à la question : « Qui va réussir ? »
?- reussit(X).

Prolog renvoie :
X = pascal ;
X = zoe.

Cela signifie que Pascal et Zoé vont réussir.

Pour vérification, on peut également tester le prédicat serieux/1 :
?- serieux(X).

Prolog répond :
X = pascal ;
X = zoe.

Ces résultats sont cohérents avec la base de connaissances :
Pascal et Zoé sont des étudiants consciencieux → 
ils font leurs devoirs → 
ils sont sérieux → 
ils révisent leurs examens → 
ils réussissent.
*/

/*
Question 3.3
?- reussit(pascal).
true.

[trace]  ?- reussit(pascal).
   Call: (12) reussit(pascal) ? creep
   Call: (13) revise(pascal) ? creep
   Call: (14) serieux(pascal) ? creep
   Call: (15) fait_devoirs(pascal) ? creep
   Call: (16) consciencieux(pascal) ? creep
   Exit: (16) consciencieux(pascal) ? creep
   Exit: (15) fait_devoirs(pascal) ? creep
   Exit: (14) serieux(pascal) ? creep
   Exit: (13) revise(pascal) ? creep
   Exit: (12) reussit(pascal) ? creep
true.

?- reussit(zoe).
true.

[trace]  ?- reussit(zoe).
   Call: (12) reussit(zoe) ? creep
   Call: (13) revise(zoe) ? creep
   Call: (14) serieux(zoe) ? creep
   Call: (15) fait_devoirs(zoe) ? creep
   Call: (16) consciencieux(zoe) ? creep
   Exit: (16) consciencieux(zoe) ? creep
   Exit: (15) fait_devoirs(zoe) ? creep
   Exit: (14) serieux(zoe) ? creep
   Exit: (13) revise(zoe) ? creep
   Exit: (12) reussit(zoe) ? creep
true.
*/

% Exercice 4
% Question 4.1
pere(pepin, charlemagne).
pere(pepin, frere_charlemagne).
pere(charlemagne, charlemagne_fils).
pere(pepin_pere, pepin).
pere(pere_berthe, berthe).
mere(berthe, charlemagne).
mere(pepin_mere, pepin).
mere(mere_berthe, berthe).

% Question 4.2
/* 
parent/2 : défini à partir de pere/2 et mere/2
parent(X,Y) si et seulement si X est le parent ou le parent de Y
*/
parent(X, Y) :- pere(X, Y).
parent(X, Y) :- mere(X, Y).

/* 
?- parent(X,charlemagne).
X = pepin ;
X = berthe.
*/

% Question 4.3
/* 
?- parent(charlemagne, X).
X = charlemagne_fils ;
false.

?- parent(pepin, Y).
Y = charlemagne ;
Y = frere_charlemagne ;
false.

?- parent(A, B).
A = pepin,
B = charlemagne ;
A = pepin,
B = frere_charlemagne ;
A = charlemagne,
B = charlemagne_fils ;
A = pepin_pere,
B = pepin ;
A = pere_berthe,
B = berthe ;
A = berthe,
B = charlemagne ;
A = pepin_mere,
B = pepin ;
A = mere_berthe,
B = berthe.
*/

% Question 4.4
/*
parents/3, tel que parents(X,Y,Z) est satisfait si X est le père de Z et Y est la mère de Z.
*/
parents(X, Y, Z) :-
    pere(X, Z),
    mere(Y, Z).

/*
?- parents(X, Y, Z).
X = pepin,
Y = berthe,
Z = charlemagne ;
X = pepin_pere,
Y = pepin_mere,
Z = pepin ;
X = pere_berthe,
Y = mere_berthe,
Z = berthe.
*/

% Question 4.5
grandPere(X, Z) :-
    pere(X, Y),
    parent(Y, Z).

grandMere(X, Z) :-
    mere(X, Y),
    parent(Y, Z).

grandParent(X, Z) :- 
    parent(X, Y), 
    parent(Y, Z).

/*
?- grandPere(X ,charlemagne_fils).
X = pepin ;
false.

?- grandMere(X ,charlemagne_fils).
X = berthe ;
false.

?- grandParent(X ,charlemagne_fils).
X = pepin ;
X = berthe ;
false.
*/

frereOuSoeur(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \== Y.

/*
?- frereOuSoeur(X, charlemagne).
X = frere_charlemagne ;
false.
*/

% Question 4.6
/* ---------------------------
   cas de base puis cas récursif
   --------------------------- */
ancetre(X, Y) :-
    parent(X, Y).                 % cas de base : X est parent direct de Y

ancetre(X, Y) :-
    parent(X, Z),
    ancetre(Z, Y).                % cas récursif : X est parent de Z qui est ancêtre de Y

/* ---------------------------
   Variante : récursif avant base
   --------------------------- */
ancetre_alt(X, Y) :-
    parent(X, Z),
    ancetre_alt(Z, Y).            % récursion en premier

ancetre_alt(X, Y) :-
    parent(X, Y).                 % base en dernier
   
/* 
?- ancetre(X, charlemagne_fils).
X = charlemagne ;
X = pepin ;
X = pepin_pere ;
X = pere_berthe ;
X = berthe ;
X = pepin_mere ;
X = mere_berthe ;
false.

?- ancetre_alt(X, charlemagne_fils).
X = pepin ;
X = pepin_pere ;
X = pere_berthe ;
X = berthe ;
X = pepin_mere ;
X = mere_berthe ;
X = charlemagne ;
false.

Commentaire :
-------------
En inversant l’ordre des propositions, Prolog utilise la recherche
en profondeur sur la clause récursive avant de vérifier le cas de base.
Cela modifie l’ordre d’apparition des solutions : les ancêtres plus éloignés
sont trouvés avant le parent direct. 

Les deux définitions produisent le même ensemble de solutions,
mais dans un ordre différent en raison de la stratégie de recherche
(profondeur d’abord, de gauche à droite).

Conclusion :
------------
- Le prédicat ancetre/2 fonctionne correctement dans les deux cas.
- La position du cas de base et du cas récursif influence uniquement
    l’ordre d’affichage des solutions, pas leur validité logique.
- La version avec le cas de base en premier est plus lisible et plus
    efficace, car elle évite de remonter inutilement la hiérarchie avant
    d’avoir trouvé les parents directs.
*/

% Exercice 5
% Question 5.1
% et (AND)
et(0,0,0).
et(0,1,0).
et(1,0,0).
et(1,1,1).

% ou (OR)
ou(0,0,0).
ou(0,1,1).
ou(1,0,1).
ou(1,1,1).

% non (NOT)
non(0,1).
non(1,0).

% Question 5.2
/*
?- et(X,Y,1).
X = Y, Y = 1.

?- et(0,0,R).
R = 0 ;
false.

?- et(X,Y,R).
X = Y, Y = R, R = 0 ;
X = R, R = 0,
Y = 1 ;
X = 1,
Y = R, R = 0 ;
X = Y, Y = R, R = 1.
*/

% Question 5.3
% ---------- Implémenter XOR en utilisant des portes de logiques ----------
xor(A,B,R) :-
    non(A,NA),
    non(B,NB),
    et(A,NB,T1),
    et(NA,B,T2),
    ou(T1,T2,R).

% ---------- Implémenter NAND en utilisant des portes de logiques ----------
nand(A,B,R) :-
    et(A,B,T),
    non(T,R).

% ---------- Implémentation de circuits: Z = NOT( NAND(X,Y) XOR NOT(X) ) ----------
circuit(X, Y, Z) :-
    nand(X, Y, N1),    % N1 = NAND(X,Y)
    non(X, NX),        % NX = NOT(X)
    xor(N1, NX, T1),   % T1 = XOR(N1, NX)
    non(T1, Z).        % Z = NOT(T1)

% Question 5.4
/*
?- circuit(0,0,Z).
Z = 1 ;
false.

?- circuit(0,1,Z).
Z = 1 ;
false.

?- circuit(1,0,Z).
Z = 0 ;
false.

?- circuit(1,1,Z).
Z = 1 ;
false.
*/

% Question 5.5
/*
1. Variable de sortie, entrées fixées:
    ?- circuit(1,0,Z).
    Z = 0 ;
    false.
Signification : Les entrées sont fixées à X=1 et Y=0, la requête permet de déterminer la sortie Z.

2. Variables d’entrée, sortie fixée:
    ?- circuit(X,Y,1).
    X = Y, Y = 0 ;
    X = 0,
    Y = 1 ;
    X = Y, Y = 1 ;
    false.
Signification : La sortie Z est fixée à 1, la requête permet de trouver toutes les combinaisons d’entrées (X,Y) qui produisent ce résultat.

3. Certaines entrées fixées, autres variables:
    ?- circuit(1,Y,Z).
    Y = Z, Z = 0 ;
    Y = Z, Z = 1 ;
    false.
Signification : L’entrée X est fixée à 1, Y et Z sont variables, la requête retourne toutes les solutions correspondantes.

4. Toutes les variables libres:
    ?- circuit(X,Y,Z).
    X = Y, Y = 0,
    Z = 1 ;
    X = 0,
    Y = Z, Z = 1 ;
    X = 1,
    Y = Z, Z = 0 ;
    X = Y, Y = Z, Z = 1 ;
    false.
Signification : Cette requête permet de générer l’ensemble de la table de vérité du circuit.
*/