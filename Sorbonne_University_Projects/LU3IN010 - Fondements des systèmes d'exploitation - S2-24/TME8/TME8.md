Lecomte Antoine & Zhang Yuxiang

TME8


Question 1.1 :

On a supposé que le tas est une zone de taille fixe égale à 128 octets.
On utilise 1 octet pour la place disponible donc il reste 127 octets (TD_max) correspondant à la taille maximale de stockage. On peut alors stocker les données dans le tas comme suit : 127 D1 D2 ... D127
On a alors libre = -1 car aucune zone libre n'est alors disponible dans le tas.


Question 1.2 :

char *p1, *p2, *p3, *p4, *p5;
Le tas est vide. libre=0. 
[128|-1]

p1 = (char *) tas_malloc(10); strcpy(p1, "tp 1");
besoin d'un octet pour la taille, comme pour toutes les futures allocations.
Donc 11 octets en tout.
128-11=117. libre=11.
[11|'tp 1'|...] [117|-1]

p2 = (char *) tas_malloc(9); strcpy(p2, "tp 2");
117-10=107. libre=21.
[11|'tp 1'|...] [10|'tp 2'|...] [107|-1]

p3 = (char *) tas_malloc(5); strcpy(p3, "tp 3");
107-6=101. libre=27.
[11|'tp 1'|...]  [10|'tp 2'|...]  [6|'tp 3'|...]  [101|-1]

tas_free(p2);
libre = 11 car la zone est libérée sur les octets 11 à 20.
[11|'tp 1'|...]  [9|libre = 27]  [6|'tp 3'|...]  [101|-1] 

p4 = (char *) tas_malloc(8); strcpy(p4, "systeme");
On utilise donc 2 octets (un pour la taille de la zone libre, un pour le pointeur sur le début de cette zone) donc il reste au final 9 octets libres dans la zone de données, c'est exactement ce qu'il nous faut.
libre = 27. Les octets 0 à 26 sont de nouveau occupés.
[11|'tp 1'|...]  [9|'systeme'|...]  [6|'tp 3'|...]  [101|-1]