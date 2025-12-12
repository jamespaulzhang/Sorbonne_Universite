Zhang Yuxiang & Lecomte Antoine

TME 2

Question 1.1 :
exécution de time sleep 5 :
sleep 5 0.00s user 0.00s system 0% cpu 5.016 total
On constate que le temps CPU passé en mode kernel et en mode user sont approximativement de 0.00s ce qui s'explique car sleep ne fait aucun calcul, donc aucune charge pour le CPU user. Pour le CPU en mode kernel, sleep suspend le processus donc le noyau n'a de même presque rien à faire. 0% cpu indique que le processus sleep n'occupe pas le processeur, il ne fait qu'attendre passivement. Il y a 16 millisecondes de latence sur la machine utilisée au moment du lancement de la commande.


Question 1.2 :
volatile est utilisé pour éviter l'optimisation par le compilateur, qui supprime la boucle si elle ne fait rien d'utile. Avec Unsigned Long Long, la valeur de max_iter est bien interprétée comme un entier de 64 bits.
Au lancement du programme, on a : ./loopcpu 6.91s user 0.01s system 96% cpu 7.152 total.
Donc le cpu est bien en mode user pour l'exécution du programme. La gestion du processus effectuée par l'OS en arrière-plan peut expliquer le temps très faible d'environ 0.01s du temps CPU passé en mode kernel. Le programme sollicite énormément le cpu durant l'exécution du programme car il a utilisé 96% des ressources du CPU. Donc le programme a utilisé 6.91 secondes de CPU pour 96% de l'usage du processeur mais l'OS a pris légèrement plus de temps pour gérer le processus correspondant aux 0.242 secondes supplémentaires et gérer d'autres tâches du système simultanément.


Question 1.3 :
On ne fait rien avec pid pour que l'appel système soit la tâche principale.
Au lancement du programme, on a : ./loopsys 0.14s user 0.01s system 38% cpu 0.398 total.
Cela indique que 0.14 secondes de temps CPU ont été utilisées pour exécuter getpid() à chaque intération. Le CPU passe alors en mode kernel mais n'a pas de tâche à effectuer donc revient immédiatement en mode user pour continuer les itérations de la boucle. Le temps total prend en compte d'autres tâches de l'OS, c'est pourquoi il est plus élevé que le temps CPU (kernel + user) lié à l'exécution du programme.


Question 2.2 :
./mytimes ls pwd nonexistent_command
Exécution de la commande : ls
loopcpu        loopsys        mytimes
loopcpu.c    loopsys.c    mytimes.c
Temps d'exécution de la commande 'ls': 0 secondes et 21232 microsecondes
Exécution de la commande : pwd
/Users/yuxiangzhang/Desktop/LU3IN010/TME2
Temps d'exécution de la commande 'pwd': 0 secondes et 7433 microsecondes
Exécution de la commande : nonexistent_command
sh: nonexistent_command: command not found
La commande 'nonexistent_command' a échoué avec le code de sortie : 127
Temps d'exécution de la commande 'nonexistent_command': 0 secondes et 7522 microsecondes
./mytimes
Aucune commande n'a été fournie.


Question 3.2 :
./mytimes "sleep 5" "sleep 10"
Exécution de la commande : sleep 5
Temps d'exécution de la commande 'sleep 5': 5 secondes et 22591 microsecondes
Exécution de la commande : sleep 10
Temps d'exécution de la commande 'sleep 10': 10 secondes et 20371 microsecondes


Question 4.1 :
./mytimes2 "ls -l" "./loopsys"
Exécution de la commande : ls -l
total 288
-rwxr-xr-x  1 yuxiangzhang  staff  16840  2  1 16:07 loopcpu
-rw-r--r--  1 yuxiangzhang  staff    182  2  1 16:06 loopcpu.c
-rwxr-xr-x  1 yuxiangzhang  staff  33432  2  1 16:34 loopsys
-rw-r--r--  1 yuxiangzhang  staff    255  2  1 16:32 loopsys.c
-rwxr-xr-x  1 yuxiangzhang  staff  33592  2  1 18:52 mytimes
-rw-r--r--@ 1 yuxiangzhang  staff   1547  2  1 18:51 mytimes.c
-rwxr-xr-x  1 yuxiangzhang  staff  33624  2  1 20:12 mytimes2
-rw-r--r--@ 1 yuxiangzhang  staff   2130  2  1 20:12 mytimes2.c
Statistiques de "ls -l" :
Temps total : 0.030000
Temps utilisateur : 0.000000
Temps systeme : 0.010000
Temps utilisateur fils : 0.000000
Temps systeme fils : 0.010000

Exécution de la commande : ./loopsys
Statistiques de "./loopsys" :
Temps total : 0.150000
Temps utilisateur : 0.000000
Temps systeme : 0.000000
Temps utilisateur fils : 0.140000
Temps systeme fils : 0.000000


Question 4.2 :
./mytimes2 "sleep 5" ./loopcpu ./loopsys
Exécution de la commande : sleep 5
Statistiques de "sleep 5" :
Temps total : 5.020000
Temps utilisateur : 0.000000
Temps systeme : 0.000000
Temps utilisateur fils : 0.000000
Temps systeme fils : 0.000000

Exécution de la commande : ./loopCPU
Statistiques de "./loopCPU" :
Temps total : 6.930000
Temps utilisateur : 0.000000
Temps systeme : 0.000000
Temps utilisateur fils : 6.910000
Temps systeme fils : 0.020000

Exécution de la commande : ./loopsys
Statistiques de "./loopsys" :
Temps total : 0.150000
Temps utilisateur : 0.000000
Temps systeme : 0.000000
Temps utilisateur fils : 0.140000
Temps systeme fils : 0.010000


Question 5.1 :
ps est de priorité 31.


Question 5.2 :
ps est toujours de priorité 31. (test effectué sous macOS)
ps est maintenant de priorité maximale : 1 (test effectué sous Linux)