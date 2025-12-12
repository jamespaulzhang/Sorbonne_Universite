TP 02

Num_Etudiant :21202829

Exo01
Question 1:
telecharger LU2IN020-TP_02.tgz et extraire l'archive dans le repertoire tp_02

Question 2:
dans le chemin tp_02/exo1 on tape la commande : cat README,pour regarder les contenu dans README,*
et apres on compile le programme mon_test.c avec la commande : gcc -o mon_test.c mon_test
et on a bien le fichier qui s'appele mon_test

Question 3:
on test le code avec le commande : ./mon_test 23
on obtient "Il n'est pas pair"
et ./mon_test 12
"Il est pair"
et ./mon_test
"Usage : mon_test <un_entier>"

Question 4:
avec la commande : mv mon_test est_il_pair ,on peut renommer l'executable en est_il_pair

./est_il_pair 12
"Il est pair"

./est_il_pair 23
"Il n'est pas pair"

./est_il_pair
"Usage : mon_test <un_entier>"

Le message d'erruer c'est pas bien le nom du fichier est_il_pair
Mais le resultat il est convenable

Question 5:
pour corrige message d'erreur correctement , on peut changer le contenu de printf dans mon_test.c avec : printf("Usage : est_il_pair <un_entier>\n");
et apres on compiler avec la commande gcc mon_test.c -o est_il_pair
et on test ./est_il_pair
Le message d'erreur est bien "Usage : est_il_pair <un entier>"

Exo 2
Question 1
pour copier est_il_pair dans repertoire exo2, on utiliser la commande : cp est_il_pair ~/tmp/ISS/tp_02/exo2
on test avec la commande :  ./est_il_pair , dans repertoire exo2,c'est bien affiche "Il est pair"

Question 2
avec la commande : est_il_pair 24 , il y a un probleme de bash : est_il_pair : commande introuvable

Question 3
on affiche la variable de $PATH avec la commande : echo $PATH
et on a : /usr/local/bin:/usr/bin:/bin:/usr/local/games:usr/games
pour sauvegarder la variable $PATH dans une variable $PATH_OLD,on doit utiliser la commande : PATH_OLD=$PATH
et voila, avec la commande : echo $PATH_OLD ,c'est bien le meme chemin que $PATH

pour ajouter le repertoire tp2/exo2 a la variable $PATH,on peut utiliser la commande:
export PATH=/users/nfs/Etu9/21202829/tmp/ISS/tp_02/exo2
et maintenant, on peut directement taper la commande : est_il_pair ,et il y a pas d'erreur comme commande introvable,et il bien affiche "Il est pair"

Question 4
On ajout '.' dans $PATH avec la commande : PATH=.:$PATH_OLD
est apres on tape la commande : est_il_pair 24,il bien s'affiche "Il est pair" sans erreur

Question 6
Il est dangereux de mettre '.' dans un PATH parce que dans le repertoire tp_02/exo2,il y a un mkdir n'importe quoi et si on ajoute '.' dans le path,tout abord il va garder cette mauvais mkdir,pas la commande mkdir donc il aurait pu effacer tous nos fichiers

Exo 03
Question 1
1.On peut creer un script fils.sh avec la commande : touch fils.sh ,et avec la commande nano fils.sh ,on peut modifier ce script
et apres nous ajoute les commandes dans ce script:
mon_pid=$$
pere_pid=$PPID
echo "Je suis $mon_pid et mon pere est $pere_pid"
2.on donne le permission d'execution au script avec la commande : chmod +x fils.sh
et nous l'execute avec la commande : ./fils.sh
Il s'affiche "Je suis 677733 et mon pere est 677572"

Question 2
1.Avec le meme etape que question 1,on creer un sript qui s'appelle pere.sh
2.On ajoute les commandes dedans:
mon_pid=$$
echo "Je suis le processus pere avec le PID $mon_pid"
for num in {1..10};do
        ./fils.sh
done
3.avec la commande : chmod +x pere.sh ,et apres la commande : ./pere.sh ,on execute le script
Il s'affiche :
Je suis le processus pere avce le PID 678249
Je suis 678250 et mon pere est 678249
Je suis 678251 et mon pere est 678249
.....
Je suis 678259 et mon pere est 678249
Donc le script pere.sh il appeler totalement 10 fois le script fils.sh

Question 3
1.On ajoute la ligne #!/bin.bash au debut de chaque script pour indiquer que ces scripts doivent etre executes avec l'interprete Bash.
2.On donne les permissions d'execution aux scripts avec la command chmod u+x pere.sh fils.sh
3.On peut maintenant executer nos scripts par ./pere,sh et ./fils.sh
Cela ne changera pas le comportement des scripts en termes de creation de processus,mais cela facilitera leur execution.

Question 4
On ajoute les commentaires avec "# ...." pour expliquer chaque etape du script.
Cela permet a quiconque lit le code de comprendre plus facilement ce que fait chaque partie du script.

Exo 04
Question 1
On va d'abord acceder dans le repertoire ~/tmp/ISS/tp_02/exo3
Avec la commande ; cp pere.sh ~/tmp/ISS/tp_02/exo4 ,on peut copier le script pere.sh dans le repertoire exo4
Quand on execute ce script il y a une erreur:
./pere.sh : ligne 9: ./fils.sh Aucun ficher ou dossier de ce type et ce message il s'affiche 10 fois
Maintenant on ajoute les commandes suivant dans le script:
if [ $# -eq 0 ]; then
        echo "Il manque un parametre"
        echo "Usage : $0 <nb_fils>"
        exit
fi
On execute ce script et il bien affiche le message d'erruer comme:
Il manque un paramètre
usage : ./pere.sh <nb_fils>

Question 2
On ajoute les commandes suivant dans le script pere.sh:
nb_fils="$1"
echo "Je suis $$"
i=1
pid_fils=$(($$+1))
while [ $i -le $nb_fils ];do
        echo "File $i : Je suis $pid_fils et mon pere est $$"
        i=$((i+1))
        pid_fils=$((pid_fils+1))
done
Maintenant on l'execute avec la commande ./pere.sh 4
Il s'affiche;
Je suis 685908
File 1 : Je suis 685909 et mon pere est 685908
File 2 : Je suis 685910 et mon pere est 685908
File 3 : Je suis 685911 et mon pere est 685908
File 4 : Je suis 685912 et mon pere est 685908