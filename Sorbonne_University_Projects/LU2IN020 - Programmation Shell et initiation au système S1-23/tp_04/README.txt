TP_04
Numero Etudiant: 21202829
Exercice 1

Question 2
Ce programme est écrit en langage C et il réalise un chiffrement de César. Voici ce que fait le programme en détail :
1. Les directives `#include` incluent les bibliothèques standard `stdlib.h` et `stdio.h`, qui fournissent des fonctions pour l'interaction avec le système d'exploitation et les entrées/sorties.
2. La fonction `main` est la fonction principale du programme. Elle prend deux arguments en ligne de commande : `argc` (le nombre d'arguments passés) et `argv` (un tableau de chaînes de caractères contenant les arguments passés).
3. Le programme vérifie si le nombre d'arguments est différent de 2. Si ce n'est pas le cas, il affiche un message d'erreur indiquant qu'une clé doit être fournie et comment utiliser le programme, puis il se termine avec le code de sortie 1 (signifiant une erreur).
4. Si une clé est fournie en argument, elle est convertie entier à chaine de caractere a l'aide de la fonction `atoi` et stockée dans la variable `cle`.
5. Ensuite, le programme entre dans une boucle `while`. Il lit un caractère à partir de l'entrée standard (fichier `stdin`) avec `fgetc`. Si la fin du fichier (`EOF`) est atteinte, la boucle se termine.
6. Pour chaque caractère lu, le programme vérifie s'il s'agit d'une lettre minuscule (`'a' <= c && c <= 'z'`). Si c'est le cas, il applique un chiffrement de César en décalant le caractère de `cle` positions dans l'alphabet modulo 26 et l'affiche. Sinon, il affiche simplement le caractère tel quel.
7. Le programme répète cette opération jusqu'à ce qu'il atteigne la fin du fichier.
8. Enfin, il retourne 0 pour indiquer qu'il s'est terminé avec succès.
En résumé, ce programme prend une clé en argument en ligne de commande, puis lit des caractères de l'entrée standard. Il chiffre les lettres minuscules en utilisant le chiffrement de César avec la clé fournie, et affiche le résultat. Les autres caractères (non alphabétiques) sont affichés tels quels. Si aucun argument n'est donné en ligne de commande, le programme affiche un message d'erreur et se termine.

Question 3
Pour quitterle programme,on utilise Cirl+d

Question 4
gcc -o cesar cesar.c
21202829@ppti-14-307-13:~/tmp/ISS/tp_04/exo1$ for i in $(seq 1 26); do echo -n "$i : " ; ./cesar $i < fenetre_sur_coquillage/part4 ; done
1 : piénfelmwpd mtyltcpd Ltyfi (lf qzcxle ELF)
2 : qjéogfmnxqe nuzmudqe Luzgj (mg radymf ELF)
3 : rképhgnoyrf ovanverf Lvahk (nh sbezng ELF)
4 : sléqihopzsg pwbowfsg Lwbil (oi tcfaoh ELF)
5 : tmérjipqath qxcpxgth Lxcjm (pj udgbpi ELF)
6 : unéskjqrbui rydqyhui Lydkn (qk vehcqj ELF)
7 : voétlkrscvj szerzivj Lzelo (rl wfidrk ELF)
8 : wpéumlstdwk tafsajwk Lafmp (sm xgjesl ELF)
9 : xqévnmtuexl ubgtbkxl Lbgnq (tn yhkftm ELF)
10 : yréwonuvfym vchuclym Lchor (uo zilgun ELF)
11 : zséxpovwgzn wdivdmzn Ldips (vp ajmhvo ELF)
12 : atéyqpwxhao xejwenao Lejqt (wq bkniwp ELF)
13 : buézrqxyibp yfkxfobp Lfkru (xr clojxq ELF)
14 : cvéasryzjcq zglygpcq Lglsv (ys dmpkyr ELF)
15 : dwébtszakdr ahmzhqdr Lhmtw (zt enqlzs ELF)
16 : exécutables binaires Linux (au format ELF)
17 : fyédvubcmft cjobjsft Ljovy (bv gpsnbu ELF)
18 : gzéewvcdngu dkpcktgu Lkpwz (cw hqtocv ELF)
19 : haéfxwdeohv elqdluhv Llqxa (dx irupdw ELF)
20 : ibégyxefpiw fmremviw Lmryb (ey jsvqex ELF)
21 : jcéhzyfgqjx gnsfnwjx Lnszc (fz ktwrfy ELF)
22 : kdéiazghrky hotgoxky Lotad (ga luxsgz ELF)
23 : leéjbahislz ipuhpylz Lpube (hb mvytha ELF)
24 : mfékcbijtma jqviqzma Lqvcf (ic nwzuib ELF)
25 : ngéldcjkunb krwjranb Lrwdg (jd oxavjc ELF)
26 : ohémedklvoc lsxksboc Lsxeh (ke pybwkd ELF)

~/tmp/ISS/tp_04/exo1$ for i in $(seq 1 26); do echo -n "$i : " ; ./cesar $i < fenetre_sur_coquillage/part1 ; done
1 : Lp Blds n'pde xêxp dzfd Wtyozhd !!!
2 : Lq Bmet o'qef yêyq eage Wuzpaie !!!
3 : Lr Bnfu p'rfg zêzr fbhf Wvaqbjf !!!
4 : Ls Bogv q'sgh aêas gcig Wwbrckg !!!
5 : Lt Bphw r'thi bêbt hdjh Wxcsdlh !!!
6 : Lu Bqix s'uij cêcu ieki Wydtemi !!!
7 : Lv Brjy t'vjk dêdv jflj Wzeufnj !!!
8 : Lw Bskz u'wkl eêew kgmk Wafvgok !!!
9 : Lx Btla v'xlm fêfx lhnl Wbgwhpl !!!
10 : Ly Bumb w'ymn gêgy miom Wchxiqm !!!
11 : Lz Bvnc x'zno hêhz njpn Wdiyjrn !!!
12 : La Bwod y'aop iêia okqo Wejzkso !!!
13 : Lb Bxpe z'bpq jêjb plrp Wfkaltp !!!
14 : Lc Byqf a'cqr kêkc qmsq Wglbmuq !!!
15 : Ld Bzrg b'drs lêld rntr Whmcnvr !!!
16 : Le Bash c'est même sous Windows !!!
17 : Lf Bbti d'ftu nênf tpvt Wjoepxt !!!
18 : Lg Bcuj e'guv oêog uqwu Wkpfqyu !!!
19 : Lh Bdvk f'hvw pêph vrxv Wlqgrzv !!!
20 : Li Bewl g'iwx qêqi wsyw Wmrhsaw !!!
21 : Lj Bfxm h'jxy rêrj xtzx Wnsitbx !!!
22 : Lk Bgyn i'kyz sêsk yuay Wotjucy !!!
23 : Ll Bhzo j'lza têtl zvbz Wpukvdz !!!
24 : Lm Biap k'mab uêum awca Wqvlwea !!!
25 : Ln Bjbq l'nbc vêvn bxdb Wrwmxfb !!!
26 : Lo Bkcr m'ocd wêwo cyec Wsxnygc !!!

Donc ligne 16 dans part4 :  exécutables binaires Linux (au format ELF)
et ligne 16 dans part4:  Le Bash c'est même sous Windows !!!
Donc on a la cle c'est 16

Question 5
avec la commande : for file in fenetre_sur_coquillage/part* ; do ./cesar 16 < $file >> news.txt ; done
Il dechiffre les ficher part1-9 dans le repertoire fenetre_sur_coquillage dans news.txt
et avec la commande : cat news.txt ,il s'affiche :
Le Bash c'est meme sous Windows !!!
Grace à Windows Subsystem for Linux (wsl),
il est aujourd'hui possible d'executer des
executables binaires Linus (au format ELF)
de manière native sur Windows 10, On peut
voir ce mècanisme comme une emulation du 
"mode user" d'un système gnu-Linux. Une fois
activé, on a accès à plusieurs distributions
intégrant Bash.

Exercice 2:
Question 1:
on ecrire le script telechargement.sh
et on donne la permission pour la commande : chmod +x telechargement.sh
et on l'execute avec : ./telechargement

Question 2:
On utilise la commande :
cat chunk/* >> fichier_reconstitue.txt

Question 3:
Pour identifier le type de fichier,on peut utilise la commande 'file' dans un terminal:
file fichier_reconstitue.txt

cette commande va analyser ce fichier et fournir des informations sur son type

si le fichier est un binaire,on peut le renommer en fonction de son type.
Par exemplee si le fichier est un fichier PDF,on peut le renommer en ajoutant l'extension '.pdf' ;
mv fichier_reconstitue.txt fichier_reconstitue.pdf
On doit assurer de renommer le fichier en fonction de son type reel,tel que determine par la commande 'file'

Question 4:
On a ecrit le script soft.sh

Exercice 3:
Question 1:
On peut utiliser la commande 'wc' en combinaison avec la redirection des flux pour n'afficher que le nombre de caracteres d'un ficher.
wc -m < test

Question 2:
On a ecrit le script biggest.sh
Il s'affiche :
dico/bien

Question 3:
On a ecrit le script selection.sh

Question 4:
Avec la commande :
./select.sh dico selection
ls selection
On peut afficher le contenu du repertoire contenant les 4 plus gros fichiers

