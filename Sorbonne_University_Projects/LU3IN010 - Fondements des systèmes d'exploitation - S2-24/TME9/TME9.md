Antoine Lecomte & Yuxiang Zhang

TME 9

Ecriture d'une stratégie de remplacement FIFO :

./mainFifo < bench
Page 1 referenced
/!\ PAGE FAULT !!! /!\
Frame 0 has been choosen
(frame 0: 1) (frame 1: _) (frame 2: _) 

Page 2 referenced
/!\ PAGE FAULT !!! /!\
Frame 1 has been choosen
(frame 0: 1) (frame 1: 2) (frame 2: _) 

Page 3 referenced
/!\ PAGE FAULT !!! /!\
Frame 2 has been choosen
(frame 0: 1) (frame 1: 2) (frame 2: 3) 

Page 1 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 3) 

Page 2 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 3) 

Page 4 referenced
/!\ PAGE FAULT !!! /!\
Frame 0 has been choosen
(frame 0: 4) (frame 1: 2) (frame 2: 3) 

Page 1 referenced
/!\ PAGE FAULT !!! /!\
Frame 1 has been choosen
(frame 0: 4) (frame 1: 1) (frame 2: 3) 

Page 2 referenced
/!\ PAGE FAULT !!! /!\
Frame 2 has been choosen
(frame 0: 4) (frame 1: 1) (frame 2: 2) 

Page 4 referenced
(frame 0: 4) (frame 1: 1) (frame 2: 2) 

Page 4 referenced
(frame 0: 4) (frame 1: 1) (frame 2: 2) 

6/10 ~ 60.000000%


Ecriture d'une stratégie de remplacement LRU :

./mainLRU < bench
Page 1 referenced
/!\ PAGE FAULT !!! /!\
Frame 0 has been choosen
(frame 0: 1) (frame 1: _) (frame 2: _) 

Page 2 referenced
/!\ PAGE FAULT !!! /!\
Frame 1 has been choosen
(frame 0: 1) (frame 1: 2) (frame 2: _) 

Page 3 referenced
/!\ PAGE FAULT !!! /!\
Frame 2 has been choosen
(frame 0: 1) (frame 1: 2) (frame 2: 3) 

Page 1 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 3) 

Page 2 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 3) 

Page 4 referenced
/!\ PAGE FAULT !!! /!\
Frame 2 has been choosen
(frame 0: 1) (frame 1: 2) (frame 2: 4) 

Page 1 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 4) 

Page 2 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 4) 

Page 4 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 4) 

Page 4 referenced
(frame 0: 1) (frame 1: 2) (frame 2: 4) 

4/10 ~ 40.000000%


Comparaison LRU/FIFO :

Le principe de FIFO est que la page qui est en mémoire depuis le plus longtemps est remplacée, tandis que pour LRU on remplace la page la moins récemment utilisée :

FIFO :
La page 4 remplace la 1 qui était là la première, on recharge la page 1 qui vient remplacer la page 2 et même chose pour la 2 qui remplace alors la page 3.
6 fautes sur 10.

LRU :
La page 4 remplace la 3 et les références se font en réduisant les remplacements inutiles puisque les références aux pages existantes ne provoquent pas de fautes.
4 fautes sur 10.

LRU est forcément plus efficace que FIFO car il conserve les pages susceptibles d'être utilisées (car elles viennent de l'être récemment), ce que FIFO ne fait pas car il peut expulser une page souvent utilisée. FIFO est plus facile à implémenter pour la gestion de mémoire que LRU mais cause plus de fautes au vu de la non-considération de l'aspect de l'utilisation récente ou ancienne.