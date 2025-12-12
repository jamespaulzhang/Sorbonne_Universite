Antoine Lecomte & Yuxiang Zhang

TME 6-7


Question 1.1 :

nb_recepteurs est modifié simultanément par plusieurs récepteurs, ce qui pose un problème de concurrence. Pour garantir la cohérence de ce compteur, il faut introduire un mécanisme de verrouillage à l'aide de sémaphores, pour permettre de synchroniser correctement les accès en écriture sur un message. On crée alors un sémaphore MUTEX qui assure qu’un seul processus (récepteur) modifie nb_recepteurs à la fois. Chaque récepteur doit acquérir MUTEX avant d'incrémenter nb_recepteurs et le libérer ensuite.

EMET (initialisé à 1) : Bloque les émetteurs lorsque le tampon est plein (ils attendent qu’il soit lu par tous les récepteurs).
RECEP[NR] (tous initialisés à 0) : Bloque chaque récepteur tant qu’un message n’est pas disponible.
MUTEX (initialisé à 1) : Garantit l’accès exclusif à nb_recepteurs.


Question 1.2 :

En utilisant plutôt un seul sémaphore RECEP, initialisé à 0 et incrémenté de NR à chaque émission, alors tous les récepteurs pourraient décrémenter ce sémaphore en même temps. Rien ne nous garantit que tous les récepteurs lisent tous le même message avant que l'émetteur n'écrase la valeur du tampon, alors qu'avec un tableau RECEP[1..NR], chaque récepteur dispose de son propre sémaphore individuel donc :
- lorsqu’un message est émis, chaque sémaphore RECEP[i] est incrémenté individuellement.
- chaque récepteur ne peut décrémenter que son propre sémaphore, ce qui garantit qu’il accède bien au bon message.
- l’émetteur est ainsi assuré que tous les récepteurs ont lu le message avant d'en envoyer un autre.

C'est le dernier récepteur qui termine la lecture du message (celui qui fait nb_recepteurs == NR) et exécute V(EMET) qui débloque l’émetteur, car une fois qu’un récepteur a lu le message, il incrémente nb_recepteurs en faisant successivement P(MUTEX), nb_recepteurs++, V(MUTEX).


Question 2.1 :

Sémaphores :

On initialise mutex_e (sémaphore pour l'écriture) à 1 pour permettre à un émetteur d'écrire dans le tampon directement. Son rôle est de garantir un accès exclusif à la section critique où l'émetteur écrit un message dans le tampon. Cela permet d'éviter qu'un autre émetteur écrive dans la même case en même temps.

mutex_r (sémaphore pour la lecture) est également initialisé à 1 pour permettre à un récepteur de lire un message immédiatement. Ce sémaphore garantit un accès exclusif à la section critique où un récepteur lit un message du tampon. Il empêche plusieurs récepteurs de lire simultanément la même case.

vide (sémaphore pour les cases vides) suit le nombre de cases vides dans le tampon. Un émetteur doit attendre qu'une case vide soit disponible avant d'écrire un message dans cette case. On l'initialise à NMAX car toutes les cases du tampon sont initialement vides.

plein (sémaphore pour les cases pleines) suit le nombre de cases pleines dans le tampon. Un récepteur doit attendre qu'une case pleine soit disponible avant de lire un message. Sa valeur initiale est 0 car 0 + NMAX = NMAX, les sémaphores vide et pleins se complètent. Il n'y a en effet aucune case pleine au début, car les émetteurs n'ont pas encore envoyé de messages.


Variables partagées :

sp->messages[NMAX] (tableau de messages) contient les messages envoyés par les émetteurs. Chaque case peut contenir un message qui sera consommé par un récepteur.
Aucune valeur particulière n'est nécessaire, car les émetteurs écrivent des valeurs aléatoires dans chaque case.

sp->nb_recepteurs[NMAX] (compteur de récepteurs) garde une trace du nombre de récepteurs ayant déjà reçu le message dans chaque case du tampon. Une fois que tous les récepteurs ont reçu un message, le compteur est réinitialisé et l'émetteur peut envoyer un nouveau message.
Il est initialisé à 0 pour chaque case (aucun récepteur n'a encore reçu le message).

sp->index_ecriture (index de l'écriture) indique la prochaine case dans le tampon où un émetteur va écrire un message.
Egalement initialisé à 0 (l'émetteur commence à écrire dans la première case).

sp->index_lecture (index de la lecture) indique la prochaine case dans le tampon qu'un récepteur va lire.
Toujours initialisé à 0 (le récepteur commence à lire dans la première case).


Question 2.2 :

Scénario illustrant comment les émetteurs et récepteurs fonctionnent dans ce système synchronisé :


Au début, toutes les cases du tampon sont vides, et les sémaphores sont configurés pour permettre aux récepteurs et aux émetteurs de travailler en synchronisation.


interaction des émetteurs en parallèle :

Les deux émetteurs commencent à fonctionner simultanément. Chaque émetteur attend qu'une case vide soit disponible (signalée par le sémaphore vide), écrit un message dans le tampon et ensuite signale que la case est pleine (en utilisant le sémaphore plein).

Puisque les émetteurs fonctionnent en parallèle, ils peuvent écrire dans le tampon sans interférer entre eux, grâce au sémaphore mutex_e qui garantit un accès exclusif à l'écriture.


interaction des récepteurs en parallèle :

Les récepteurs attendent qu'une case pleine soit disponible (signalée par le sémaphore plein), puis lisent le message dans cette case.

Chaque récepteur incrémente son propre compteur dans nb_recepteurs pour indiquer qu'il a consommé ce message, mais aucun récepteur ne peut lire la même case en même temps, car le sémaphore mutex_r garantit un accès exclusif à chaque case pendant la lecture.


émetteurs-récepteurs:

Lorsqu'un récepteur a consommé un message, il vérifie si tous les récepteurs ont bien consommé ce message (en vérifiant si nb_recepteurs a atteint la valeur de NR). Si c'est le cas, le récepteur réinitialise le compteur pour cette case, indique que la case est maintenant vide (en utilisant le sémaphore vide), et met à jour l'index de lecture pour pointer vers la prochaine case.

Une fois que tous les récepteurs ont consommé le message, l'émetteur peut commencer à écrire un nouveau message dans la case vide, ce qui garantit que les récepteurs n'ont pas de conflits pour lire un message et que chaque message est complètement écrit avant qu'un nouveau message ne le soit à son tour.