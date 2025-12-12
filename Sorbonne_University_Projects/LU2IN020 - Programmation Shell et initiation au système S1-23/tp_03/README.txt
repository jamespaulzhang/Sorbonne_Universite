TP_03

Numero Etudiant : 21202829

Exo_01:
Question 1:
On implemente un programme helloYou en C
#include <stdio.h>
#include <stdlib.h>

int main(int argc,char const *argv[]){
  for (int i = 1; i < argc; ++i){
    printf("%s\n",argv[i]);
  }
  return 0;
}

Question 2:
on ajoute un message d'erreur s'il n'y a personne a saluer:

if (argc < 2){
  printf("Personne a saluer\n");
  printf("Usage : %s <personne a saluer>\n",argv[0]);
  exit(1);
}
on le compiler avec la commande : gcc -o helloYou helloYou.c
et on le test avec:
./helloYou
et il affiche bien un message d'erreur:
Personne a saluer
Usage : ./helloYou <personne a saluer>

et on le test avec:
./helloYou Pierre Sylvain Étienne Manon Maxime
il s'affiche bien:
Pierre
Sylvain
Étienne
Manon
Maxime

Question 3:
avec /helloYou Pierre Sylvain Étienne Moustache Manon Lanza Maxime Biaggi
Il s'affiche un ligne Nom et un autre ligne Prenom:
Pierre
Sylvain
Étienne
Moustache
Manon
Lanza
Maxime
Biaggi

Si on veut regler ce probleme,il faut on ajoute "" devant chaque nom et apres chaque Prenom comme:
./helloYou "Pierre Sylvain" "Étienne Moustache" "Manon Lanza" "Maxime Biaggi"
et il s'affiche bien:
Pierre Sylvain
Étienne Moustache
Manon Lanza
Maxime Biaggi

Exercice 2
Question 1:
On implemente un programme somme en C:
#include <stdio.h>
#include <stdlib.h>

int main(int argc,char const *argv[]){

  if (argc < 2){
    printf("Il faut au moins un parametre\n");
    printf("Usage : %s <argument>\n",argv[0]);
    exit(1);
  }

  int res = 0;
  for (int i = 1; i < argc; ++i){
    res += atoi(argv[i]);
  }
  printf("La somme des parametres est: %d\n",res);
  return 0;
}

Question 2:
type true;type false
true est une primitive du shell
false est une primitive du shell
La commande 'true' retourne toujours la valeur 0,ce qui signifie success,et 'false' retourne toujours un valeur different que 0,ce qui signifie un echec

Question 3:
On implemente un script addition.sh:
#!/bin/bash
while true; do
        echo -n "Saisissez un nombre ou 'q' pour quitter : "
        read maVariable
        if test "$maVariable" = "q"; then
                break
        fi

        echo "Vous avez ajoute $maVariable a la somme"

done

/addition.sh
Saisissez un nombre ou 'q' pour quitter : 12
Vous avez ajoute 12 a la somme
Saisissez un nombre ou 'q' pour quitter : 30
Vous avez ajoute 30 a la somme
Saisissez un nombre ou 'q' pour quitter : q

et avec Cirl+c,on peut arreter notre programme:
./addition.sh
Saisissez un nombre ou 'q' pour quitter : ^C

Question 4:
On ajoute :
#!/bin/bash

while true; do
        echo -n "Saisissez un nombre ou 'q' pour quitter : "
        read maVariable
        if test "$maVariable" = "q"; then
                break
        fi
        somme=$((somme+maVariable))
        echo "Vous avez ajoute $maVariable a la somme"
        ./somme $somme
done

Si on appele le programme 'somme' a chaque tour de boucle,un nouveau processus serait cree a chaque fois.
Donc,le nombre total de processus crees dependrait du nombrede tours de boucle.


Quetsion 5:
-----------------------------------------------------------
#!/bin/bash

while true; do
        echo -n "Saisissez un nombre ou 'q' pour quitter : "
        read maVariable
        if test "$maVariable" = "q"; then
                break
        fi
        echo "Vous avez ajoute $maVariable a la somme"
        somme=$((somme+maVariable))
done
./somme $((somme+maVariable))
------------------------------------------------------------

#!/bin/bash

old=0

while read maVariable; do

        if test "$maVariable" = "q"; then
                break
        fi

        old="$old $maVariable"

        echo "Vous avez ajoute $maVariable a la somme"
done

./somme $old

Exercice 3
Question 1:
On ecrire un programme C qui s'appele monEnvironnement.c suivant:
#include <stdio.h>
#include <stdilb.h>

int main(){
        char* home = getenv("HOME");
        char* path = getenv("PATH");
        char* pwd = getenv("PWD");

        printf("Contenu de HOME : %s\n",home);
        printf("Contenu de PATH : %s\n",path);
        printf("Contenu de PWD : %s\n",pwd);

        return 0;
}

Dans le chemin ~/tmp/ISS/tp_03
On le compiler avec la commande : gcc -o monEnvironnement monEnvironnement.c
Et on l'execute avec la commande : ./monEnvironnement
Il s'affiche bien :
Contenu de HOME : /users/Etu9/21202829
Contenu de PATH : /usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
Contenu de PWD : /users/Etu9/21202829/tmp/ISS/tp_03

Et on utilise la commande : cd .. ,pour aller dans le repertoire parent ~/tmp/ISS
et on le lance en utilisant un chemin vers le binaire correspondant au programme ; ~/tmp/ISS/tp_03/monEnvironnement

Contenu de HOME : /users/Etu9/21202829
Contenu de PATH : /usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games
Contenu de PWD : /users/Etu9/21202829/tmp/ISS

Question 2:
On ajoute les lignes suivants dans monENvironnement.c :
char* test1 = getenv("TEST_1");
char* test2 = getenv("TEST_2");
char* test3 = getenv("TEST_3");

printf("Contenu de TEST_1 : %s\n",test1);
printf("Contenu de TEST_2 : %s\n",test2);
printf("Contenu de TEST_3 : %s\n",test3);

puis on le compile et l'execute pour la premiere fois:
1.Il s'affiche le meme HOME,PATH,PWD,mais (null) dans chaque contenu de TEST_[1-3]
2.Ensuite,on utilise la commande : export TEST_1="J'existe" ,on define la variable d'environnement TEST_1 avec "J'existe"
et on l'execute,maintenant dans le contenu TEST_1,il s'affiche bien "J'existe",et pour les contenus de TEST_2 et TEST_3,sont encore (null)
3.Et on l'execute encore une fois,le contenu de TEST_1 reste le meme comme "J'existe"
4.Avec la commade : TEST_2="J'existe" ./monEnvironnement
Il s'affiche temporairement le contenu de TEST_2 est "J'existe"
5.Et on l'execute ce programme encore une fois,le contenu de TEST_2 disparu,donc maintenant que le contenu de TEST_1 reste "J'existe" ,et les contenus de TEST_2 et TEST_3 sont (null)

Remarque:
Si on veut declarer une variable d'environnement pas temporairement,on dois utiliser la commande 'export'

Question 3:
Avec la commande : echo $TEST_1
Il s'affiche bien ; J'existe
Et la commande : echo $TEST_2 ,Il s'affiche rien car on a declare la variable d'environnement TEST_2 avec "J'existe" temporairement
Maintenant on utilise la commande 'env' ,il s'affiche l'ensemble des variables d'environnement
Donc on peux verifier simplement que la presence de la variable TEST_1=J'existe
Mais TEST_2 n'est pas dans l'ensemble des variables d'environnement

Question 4:
Pour tester si la commande 'env'n'est pas un builtin,on utilise la commande : type env
Il s'affiche : env est haché (/usr/bin/env)
Le fait que 'env' ne soit pas un builtin signfie qu'il est un executable separe present dans le systeme de fichers.
Il est generalement situe dans le repertoire /usr/bin/ ou un autre repertoire specifie dans la variable d'environnement 'PATH'

Question 5;
Avec la commande : unset TEST_1 ,on peut supprimer la variable TEST_1
Et on verifier avec la commande : env ,on peut voir que la variable d'environnement TEST_1 est disparu

Question 6;
Pour tester le type de la commande 'unset',on doit utiliser la commande : type unset
Il s'affiche ; unset est une primitive du shell
Donc unset est un builtin pas une commande exterieure
Explication du choix:
1.Manipulation des variables
2.Gestion interne des variables
3.Efficacite
