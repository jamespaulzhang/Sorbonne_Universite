Yuxiang Zhang & Antoine Lecomte

TME3

Question 1.3 :

Avec un quantum de 0.3s :

./main
RANDOM Election !
Proc. Court1 - 0
Proc. Court1 - 10000000
Proc. Court1 - 20000000
Proc. Court1 - 30000000
Proc. Court1 - 40000000
Proc. Court1 - 50000000
Proc. Court1 - 60000000
Proc. Court1 - 70000000
Proc. Court1 - 80000000
Proc. Court1 - 90000000
############ FIN COURT 1

RANDOM Election !
Proc. Court0 - 0
Proc. Court0 - 10000000
Proc. Court0 - 20000000
Proc. Court0 - 30000000
Proc. Court0 - 40000000
Proc. Court0 - 50000000
Proc. Court0 - 60000000
Proc. Court0 - 70000000
Proc. Court0 - 80000000
Proc. Court0 - 90000000
############ FIN COURT 0

RANDOM Election !
Proc. Long0 - 0
Proc. Long0 - 40000000
Proc. Long0 - 80000000
Proc. Long0 - 120000000
Proc. Long0 - 160000000
RANDOM Election !
Proc. Long1 - 0
Proc. Long1 - 40000000
Proc. Long1 - 80000000
Proc. Long1 - 120000000
Proc. Long1 - 160000000
RANDOM Election !
Proc. Long1 - 200000000
Proc. Long1 - 240000000
Proc. Long1 - 280000000
Proc. Long1 - 320000000
Proc. Long1 - 360000000
RANDOM Election !
############ FIN LONG 1

RANDOM Election !
Proc. Long0 - 200000000
Proc. Long0 - 240000000
Proc. Long0 - 280000000
Proc. Long0 - 320000000
Proc. Long0 - 360000000
RANDOM Election !
############ FIN LONG 0

PID	FUNCTION	REAL-TIME	CPU-TIME	WAITING-TIME
--------------------------------------------------------------------
0	Function0	1.745s		0.657s		1.088s
1	Function1	1.388s		0.654s		0.734s
2	Function2	0.434s		0.170s		0.264s
3	Function3	0.264s		0.264s		0.000s
--------------------------------------------------------------------
Average:		0.958s		0.436s		0.521s
--------------------------------------------------------------------

Avec un quantum de 4s :
Moins d'élections.

Avec un quantum de 0.01s :
On obtient plus d'élections.


Question 2.2 : (SJFElect)

PID	FUNCTION	REAL-TIME	CPU-TIME	WAITING-TIME
--------------------------------------------------------------------
0	Function0	1.938s		1.938s		0.000s
1	Function1	4.324s		1.841s		2.483s
2	Function2	2.073s		0.135s		1.938s
3	Function3	1.651s		0.136s		1.515s
4	Function4	1.328s		0.138s		1.189s
5	Function5	1.004s		0.136s		0.868s
6	Function6	1.978s		0.137s		1.841s
7	Function7	1.655s		0.137s		1.518s
8	Function8	1.348s		0.154s		1.194s
9	Function9	1.035s		0.145s		0.890s
--------------------------------------------------------------------
Average:		1.833s		0.490s		1.344s
--------------------------------------------------------------------


Question 3.2 : (ApproxSJF)

PID	FUNCTION	REAL-TIME	CPU-TIME	WAITING-TIME
--------------------------------------------------------------------
0	Function0	3.643s		1.944s		1.699s
1	Function1	4.901s		1.985s		2.916s
2	Function2	2.136s		0.136s		2.000s
3	Function3	1.719s		0.137s		1.582s
4	Function4	1.426s		0.153s		1.273s
5	Function5	1.099s		0.137s		0.963s
6	Function6	0.734s		0.137s		0.597s
7	Function7	1.058s		0.137s		0.922s
8	Function8	0.734s		0.137s		0.597s
9	Function9	0.677s		0.137s		0.540s
--------------------------------------------------------------------
Average:		1.813s		0.504s		1.309s
--------------------------------------------------------------------


(l'algorithme aléatoire)

PID	FUNCTION	REAL-TIME	CPU-TIME	WAITING-TIME
--------------------------------------------------------------------
0	Function0	4.227s		1.953s		2.274s
1	Function1	3.136s		1.853s		1.282s
2	Function2	1.141s		0.141s		1.000s
3	Function3	0.728s		0.141s		0.587s
4	Function4	3.217s		0.136s		3.080s
5	Function5	2.885s		0.136s		2.749s
6	Function6	1.062s		0.138s		0.924s
7	Function7	2.099s		0.136s		1.963s
8	Function8	1.604s		0.137s		1.467s
9	Function9	0.596s		0.136s		0.460s
--------------------------------------------------------------------
Average:		2.069s		0.491s		1.579s
--------------------------------------------------------------------


Les temps d'attente moyens sont assez proches : 2.069s pour l'algorithme aléatoire contre 1.813s pour ApproxSJF.
Temps d'attente CPU moyen : Algorithme aléatoire : 0.491s, ApproxSJF : 0.504s.
Le temps d'attente est de 1.579s toujours en moyenne pour l'algorithme aléatoire et de 1.309s pour ApproxSJF.
ApproxSJF semble plus efficace que l'algorithme aléatoire sur le temps d'exécution en totalité et attend moins longtemps que l'algorithme aléatoire. Bien que l'algorithme aléatoire montre un temps CPU légèrement inférieur à ApproxSJF, il s'exécute plus lentement que celui-ci et donc ApproxSJF est à privilégier dans la plupart des cas, notamment dans des cas d'utilisation où il est important de limiter au maximum le temps d'attente (dans un programme qui par exemple demande beaucoup de passages en attente des processus).


Question 3.3 :

ApproxSJF peut provoquer une famine pour des processus plus longs, dans le cas où des processus plus courts arrivent en continu, ce qui a pour effet de repousser continuellement ces processus plus longs qui n'arrivent pas à arriver à terme de leur exécution, car l'algorithme ApproxSJF choisit toujours le processus avec la plus courte durée de traitement (ou consommation CPU la plus faible) donc les processus longs peuvent ne jamais être sélectionnés s'il y a toujours des processus plus courts en attente. Au contraire, l'algorithme aléatoire n'a pas ce problème.

ApproxSJF initial (peut provoquer une famine) : 

int ApproxSJF(void) {
  int i, p = -1;

  // Trouver le premier processus en état RUN
  for (i = 0; i < MAXPROC; i++) {
      if (Tproc[i].flag == RUN) {
          p = i;
          break;
      }
  }

  // Si aucun processus n'est en état RUN, retourner -1 (aucune élection possible)
  if (p == -1) {
      return -1;
  }

  // Parcourir les processus restants pour trouver celui avec la plus courte durée
  for (; i < MAXPROC; i++) {
      if (Tproc[i].flag == RUN && Tproc[i].ncpu < Tproc[p].ncpu) {
          p = i;
      }
  }

  return p;
}


Désormais, le procédé de vieillissement pour augmenter la priorité d'un processus qui a passé plus ou moins de temps en attente est appliqué sur la nouvelle version de la fonction (voir dans le fichier scen.c). Nous avons utilisé un facteur d'augmentation de priorité de 0.2 pour chaque seconde d'attente à titre d'exemple. L'effet de cette modification est que les processus qui attendent longtemps voient leur priorité augmentée, même s'ils ont des durées CPU plus longues et nous avons maintenant la garantie que tous les processus seront finalement exécutés. Plus ce coefficient est important, plus le risque de famine est faible, mais cela diminue l'efficacité de l'algorithme ApproxSJF.