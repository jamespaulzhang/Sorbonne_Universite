TP_01

Num Etudiant: 21202829 & 21218303

Exo 01:

Q1:
En utilisant la commande cd .. plusieurs fois,nous finison par atteindre la racine du systeme
,qui est representee par 21202829@ppti-14-307-13:/$
si nous encore le tapons,il ne peut pas remonter au-dela de la racine du systeme.

Q2:
Si nous executons la commande cd sans parametre
,cela nous ramenera a notre repertoire personnel(Home):21202829@ppti-14-307-13:~$

Q3:
Nous pouvons retourner a la racine en utilisant la commande:cd /

Q4:
Nous pouvons utiliser la touche tabulation pour auto_completer les noms de repertoires.
Par exemple,il y a un sous_repertoire nomme "Documents",nous pouvons taper:"cd Doc",et ensuiteappuyer sur la touche tabulation "<TAB>",pour auto_completer le nom.
cd Doc<TAB> <=> cd Documents

Q5:
ls ./toto/titi fait reference a un chemin relatif a partir du repertoire courant.Il essaie de lister le contenu du repertoire titi qui se trouve dans le repertoire toto,qui lui-meme se tro>ls ~/toto/titi utilise le chemin complet(absolu) en commencant par le repertoire personnel(Home) de l'utilisateur.Il essaie de lister le contenu du repertoire titi qui se trouve dans le re>ls ../toto/titi utilise un chemin relatif en remontant d'un niveau (../) par rapport au repertoire courant. Il essaie de lister le contenu du repertoire titi qui se trouve dans le repertoi>Conclusion: Le Bash interprete les chemins de maniere relative ou absolue en fonction de la maniere dont ils sont specifiques dans la commande. Le caractere ~ fait reference au repertoire >

Exo 02:
Q1:
La commande mkdir permet de creer ler repertoires dont les chemins sont passes en parametre.
La commande :"mkdir /tmp/rep1/rep2" pose un problem :impossible de creer le repertoire< /tmp/rep1/rep2 >:Aucun fichier ou dossier de ce type.
Solution: Avec la commande: mkdir -p tmp/rep1/rep2 , on peut realiser cette operation.

Q2:
Avec la commande: mkdir -p  ~/LU2IN020/tp_01/{exo_03,exo_04} ~/LU2IN020/{tp_02,tp_03,tp_04,tp_11},on peut creer tous les repertoires specifies en chemin.
Et on peut le verifier en utilisant la commande tree; tree LU2IN020 ,qui affiche l'arborescene des fichers

Exo 03:
Q1:
~$ wget https://julien.sopena.fr/LU2IN020-TP_01-EXO_03.tgz
--2023-09-17 17:28:33-- https://julien.sopena.fr/LU2IN020-TP_01-EXO_03.tgz
Resolution de julien.sopena.fr (julien.sopena.fr)... 90.22.224.44
Connexion a julien.sopena.fr (julien.sopena.fr)|90.22.224.44|:443...

Q2:
La commande: tar tzf LU2IN020-TP_01-EXO_03.tgz ,c'est pour afficher le contenu de l'archive
La commande: tar xzf LU2IN020-TP_01-EXO_03.tgz ,c'est pour extraire les fichiers de l'archive

Q3:
La commande: rm LU2IN020-TP_01-EXO_03.tgz ,c'est pour supprimer l'archive

Q4;
La commande: cat README ,c'est pour afficher le contenu du ficher README

Exo 04:
Q1:
wget https://julien.sopena.fr/LU2IN020-TP_01-EXO_04.tgz //Placer le contenu de l'archive
tar xzf LU2IN020-TP_01-EXO_04.tgz //Extraire les fichiers dans l'archive
rm LU2IN020-TP_01-EXO_04.tgz //Supprimer l'archive

Q2:
Avec la commande :rm *.log ,sans le flag -f,elle demande une confirmation avant de supprimer chaque fichier.
Si aucun fichier correspondant a '*.log'n'est trouve,'rm'affichera un message d'erreur mais ne supprimera rien.
En resume,la principale difference est que 'rm -f *.log'est plus agressif et ne demande pas de confirmation,meme en cas d'erreur,tandis que 'rm' seul demandera confirmation pour chaque fic>
Q3:
Avec la commande: 'rm -f error.flac *.flac' ou 'rm error.flac *.flac'

Q4:
Pour creer un fichier nomme 'infos_1001_album.sh' dans le repertoire'exo_04',il faut avec la commande :
touch ~/LU2IN020/tp_01/exo_04/infos_1001_album.sh
Et apres nous ajoutrons les commandes suivants:
#!/bin/bash

# Affichage des albums des Beatles
echo "Les albums recommandes des Beatles sont:"
ls -1 | grep "Beatles"

#Fin du script

Q5:
#Affichage des albums d'une seule lettre
echo "les albums d'une seule lettre sont :"
ls -1 | grep "^[A-Z]$"

Q6:
#Comptage des albums
count=$(ls -1 | wc -1)
echo "Il y a $count albums dans la selection."

Q7:
#Calcul de la moyenne des tailles des noms de fichiers
total=0
for file in *; do
        total=$((total + ${#file}))
done

average=$((total / count))
echo "La moyenne des tailles des noms de fichiers est de $average caracteres."

Q8:
#Affichage de la repartition des albums par annee
echo "Repartition des albums par annee:"
for year in {1995..2016}; do
        count=$(ls -1 | grep "$year" | wc -1)
        echo "$year : $(seq -s 'x' $count)"
done

Q9;
touche ~LU2IN020/tp_01/exo_04/sort_album_by_year.sh #creer un nouveau fichier

#!/bin/bash

#Creation des repertoires par annee
for year in {1955..2016}; do
        mkdir -p by_year/$year
done

#Copie des albums dans les repertoires correspondants a leur annee
for file in *.flac; do
        year=$(echo $file | cut -d'_' -f3)
        cp $file by_year/$year/
done

Ensuite,execute le script avec cette commande: bash sort_album_by_year.sh