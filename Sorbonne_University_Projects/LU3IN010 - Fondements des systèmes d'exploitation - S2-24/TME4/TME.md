Yuxiang Zhang & Antoine Lecomte

TME 4


Exercice 1 :

Multi-grep simple : multi-grep.c.

./mg "erreur" file1.txt file2.txt file3.txt file4.txt
grep: file4.txt: Aucun fichier ou dossier de ce type
Processus fils 196843 terminé avec le code 0
Processus fils 196844 terminé avec le code 0
Processus fils 196845 terminé avec le code 1
Processus fils 196846 terminé avec le code 2

0 : motif trouvé
1 : motif absent
2 : fichier inexistant


Exercice 2 & 3 :

Multi-grep à parallélisme contraint avec affichage des statistiques : multi-grep_2.c.

./mg2 "erreur" file1.txt file2.txt file3.txt file4.txt
Processus fils 196922 terminé avec le code 0
Statistiques pour le processus fils 196922 :
  Temps CPU utilisateur : 0.001509 secondes
  Temps CPU système   : 0.000000 secondes
Processus fils 196923 terminé avec le code 0
Statistiques pour le processus fils 196923 :
  Temps CPU utilisateur : 0.001835 secondes
  Temps CPU système   : 0.000000 secondes
Processus fils 196924 terminé avec le code 1
Statistiques pour le processus fils 196924 :
  Temps CPU utilisateur : 0.001510 secondes
  Temps CPU système   : 0.000000 secondes
grep: file4.txt: Aucun fichier ou dossier de ce type
Processus fils 196925 terminé avec le code 2
Statistiques pour le processus fils 196925 :
  Temps CPU utilisateur : 0.000000 secondes
  Temps CPU système   : 0.001421 secondes


./mg2 "erreur" file1.txt file2.txt file3.txt file4.txt
Processus fils 197373 terminé avec le code 0
Statistiques pour le processus fils 197373 :
  Temps CPU utilisateur : 0.000000 secondes
  Temps CPU système   : 0.001516 secondes
Processus fils 197374 terminé avec le code 0
Statistiques pour le processus fils 197374 :
  Temps CPU utilisateur : 0.001485 secondes
  Temps CPU système   : 0.000000 secondes
Processus fils 197375 terminé avec le code 1
Statistiques pour le processus fils 197375 :
  Temps CPU utilisateur : 0.000000 secondes
  Temps CPU système   : 0.001488 secondes
grep: file4.txt: Aucun fichier ou dossier de ce type
Processus fils 197376 terminé avec le code 2
Statistiques pour le processus fils 197376 :
  Temps CPU utilisateur : 0.001468 secondes
  Temps CPU système   : 0.000000 secondes


Les résultats diffèrent entre les exécutions. Pour le processus fils 197376 (Code 2), le temps est en utilisateur, ce qui est inhabituel pour un fichier inexistant. Cela pourrait indiquer que grep a fait un pré-traitement avant de réaliser que le fichier était manquant, ou qu'il y a eu un léger délai avant l'échec.
Nos fichiers sont très petits, donc cela peut expliquer pourquoi le traitement est rapide et passe davantage en mode système, car pour des fichiers volumineux, le CPU serait surtout en mode user.


Exercice 4 :

Un processus zombie est un processus qui a terminé son exécution, mais qui reste encore dans la table des processus du système d'exploitation parce que son parent n'a pas encore récupéré son code de retour. Le parent doit toujours nettoyer ses processus fils avec wait(). Le processus init adopte un processus fils si son parent a été supprimé avant de supprimer son fils, qui se chargera de le faire à sa place.


./zb
Les processus fils sont maintenant des zombies pendant 10 secondes.
Premier processus fils (PID: 198052) en cours de terminaison.
Second processus fils (PID: 198053) en cours de terminaison.
Le premier processus terminé est le FILS 1 (PID 198052)
Le second processus terminé est le FILS 2 (PID 198053)
Tous les processus fils sont terminés.

Les 3 dernières lignes sont affichées après le sleep(10).