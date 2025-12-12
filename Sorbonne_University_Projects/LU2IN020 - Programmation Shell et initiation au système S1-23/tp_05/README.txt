TP_05
Numero etudiant: 21202829

Exercice 1:
Question 1 :  
Pour récupérer les données, on utilise la commande: wget http://julien.sopena.fr/LU2IN020-TP_04.tgz && tar -zxvf LU2IN020-TP_04.tgz

Question 2 : 
Pour récupérer les sources du projet cowsay depuis le dépôt Git, on utilise la commande:
git clone https://github.com/schacon/cowsay.git

Question 3 : 
On accede dans le répertoire cowsay avec la commande : cd cowsay
et apres on lance le script install.sh en spécifiant le répertoire d'installation avec la commande : ./install.sh ~/usr
Une fois l'installation terminée, on peut supprimer le répertoire cowsay qu'on as cloné.

Question 4 : 
Pour nou assurer que on peut lancer cowsay depuis n'importe quel endroit, on doit nous assurer que le chemin vers ~/usr/bin est inclus dans notre variable $PATH,avec la commande suivant
export PATH=$PATH:~/usr/bin

Question 5 : 
On ecrire le script jungle.sh :
#!/bin/bash

# Demander à l'utilisateur de choisir entre VF et VO
read -p "Choisissez entre VF et VO : " choix

# Parcourir le fichier CSV et exécuter cowsay avec les paramètres appropriés
while IFS=',' read -r animal cri_VF cri_VO; do
    if [ "$choix" = "VF" ]; then
        cowsay -f "$animal" "$cri_VF"
    elif [ "$choix" = "VO" ]; then
        cowsay -f "$animal" "$cri_VO"
    else
        echo "Choix invalide. Veuillez entrer VF ou VO."
        exit 1
    fi
done < blabla.csv
Ce script lit le blabla.csv situé dans le répertoire exo1 et exécute la commande cowsay avec les paramètres appropriés en fonction du choix de l'utilisateur entre VF et VO. 
Avec la commande: chmod +x jungle.sh, on peut donner les permissions d'exécution pour ce script

On peut tester le cowsay et le jungle.sh:
$ cowsay Hello,world!
 ______________
< Hello,world! >
 --------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||

$ ./jungle.sh
Choisissez entre VF et VO : VF
 _____________
< Mugissement >
 -------------
  \
   \    (__)
        o o\
       ('') \---------
          \           \
           |          |\
           ||---(  )_|| *
           ||    UU  ||
           ==        ==
 ____________
< Coassement >
 ------------
     \
      \
          oO)-.                       .-(Oo
         /__  _\                     /_  __\
         \  \(  |     ()~()         |  )/  /
          \__|\ |    (-___-)        | /|__/
          '  '--'    ==`-'==        '--'  '
 ______________
< Clapissement >
 --------------
  \
   \   \
        \ /\
        ( )
      .( o ).
 ______________
< Barrissement >
 --------------
 \     /\  ___  /\
  \   // \/   \/ \\
     ((    O O    ))
      \\ /     \ //
       \/  | |  \/
        |  | |  |
        |  | |  |
        |   o   |
        | |   | |
        |m|   |m|
 ___________
< Hurlement >
 -----------
  \
   \
       ___
     {~._.~}
      ( Y )
     ()~*~()
     (_)-(_)
 ___________
< Feulement >
 -----------
  \
   \ ,   _ ___.--'''`--''//-,-_--_.
      \`"' ` || \\ \ \\/ / // / ,-\\`,_
     /'`  \ \ || Y  | \|/ / // / - |__ `-,
    /@"\  ` \ `\ |  | ||/ // | \/  \  `-._`-,_.,
   /  _.-. `.-\,___/\ _/|_/_\_\/|_/ |     `-._._)
   `-'``/  /  |  // \__/\__  /  \__/ \
        `-'  /-\/  | -|   \__ \   |-' |
          __/\ / _/ \/ __,-'   ) ,' _|'
         (((__/(((_.' ((___..-'((__,'
 ____________
< Grognement >
 ------------
       \    ____
        \  /    \
          | ^__^ |
          | (oo) |______
          | (__) |      )\/\
           \____/|----w |
                ||     ||

                 Moofasa
 ___________
< Bêlement >
 -----------
  \
   \   \_\_    _/_/
    \      \__/
           (oo)\_______
           (__)\       )\/\
               ||----w |
               ||     ||
 ___________
< Bêlement >
 -----------
  \
   \
       __
      UooU\.'@@@@@@`.
      \__/(@@@@@@@@@@)
           (@@@@@@@@)
           `YY~~~~YY'
            ||    ||
 ____________
< Sifflement >
 ------------
  \
     \
                  _ _
       | __/|  .~    ~.
       /oo `./      .'
      {o__,       {
        / .  . )
        `-` '-'     }
       .(   _(   )_.'
      '---.~_ _ _|

 ________________
< Glougloutement >
 ----------------
  \                                  ,+*^^*+___+++_
   \                           ,*^^^^              )
    \                       _+*                     ^**+_
     \                    +^       _ _++*+_+++_,         )
              _+^^*+_    (     ,+*^ ^          \+_        )
             {       )  (    ,(    ,_+--+--,      ^)      ^\
            { (@)    } f   ,(  ,+-^ __*_*_  ^^\_   ^\       )
           {:;-/    (_+*-+^^^^^+*+*<_ _++_)_    )    )      /
          ( /  (    (        ,___    ^*+_+* )   <    <      \
           U _/     )    *--<  ) ^\-----++__)   )    )       )
            (      )  _(^)^^))  )  )\^^^^^))^*+/    /       /
          (      /  (_))_^)) )  )  ))^^^^^))^^^)__/     +^^
         (     ,/    (^))^))  )  ) ))^^^^^^^))^^)       _)
          *+__+*       (_))^)  ) ) ))^^^^^^))^^^^^)____*^
          \             \_)^)_)) ))^^^^^^^^^^))^^^^)
           (_             ^\__^^^^^^^^^^^^))^^^^^^^)
             ^\___            ^\__^^^^^^))^^^^^^^^)\\
                  ^^^^^\uuu/^^\uuu/^^^^\^\^\^\^\^\^\^\
                     ___) >____) >___   ^\_\_\_\_\_\_\)
                    ^^^//\\_^^//\\_^       ^(\_\_\_\)
                      ^^^ ^^ ^^^ ^
 _____
< ??? >
 -----
   \
    \
        .--.
       |o_o |
       |:_/ |
      //   \ \
     (|     | )
    /'\_   _/`\
    \___)=(___/

Exercice 2
Question 1
last -da > connexions.log

Question 2
On ecrire le script trace.sh:

#!/bin/bash

function usage() {
    echo "Usage: $0 <fichier_logs>"
    exit 1
}

if [ $# -ne 1 ]; then
    echo "Erreur : veuillez spécifier un fichier de logs."
    usage
fi

if [ ! -r "$1" ]; then
    echo "Erreur : le fichier $1 n'est pas accessible en lecture."
    usage
fi

Question 3
nb_entrees=$(grep -c "pts" "$1")
echo "Nombre d'entrées : $nb_entrees"

Question 4
utilisateur=$(whoami)
dernier_utilisateur=$(head -n 1 "$1" | cut -d ' ' -f 1)
if [ "$utilisateur" = "$dernier_utilisateur" ]; then
    echo "Vous êtes le dernier à vous être connecté."
else
    echo "Vous n'êtes pas le dernier à vous être connecté."
fi

Question 5
nb_connexions=$(grep -c "$utilisateur" "$1")
echo "Nombre de connexions pour $utilisateur : $nb_connexions"

Question 6
nb_utilisateurs=$(cut -d ' ' -f 1 "$1" | sort | uniq | wc -l)
echo "Nombre d'utilisateurs différents : $nb_utilisateurs"

Question 7
nb_machines=$(cut -d ' ' -f 3 "$1" | sort -u | grep -cvE '0.0.0.0|localhost')
echo "Nombre de machines distantes : $nb_machines"

Question 8
utilisateurs_distants=$(cut -d ' ' -f 1,3 "$1" | grep -vE '0.0.0.0|localhost' | sort -u | cut -d ' ' -f 1)
for utilisateur_distant in $utilisateurs_distants; do
    echo "Connexions de $utilisateur_distant :"
    grep "$utilisateur_distant" "$1" | cut -d ' ' -f 3 | sort -u
    echo
done

Question 10
Avec la commande finger apres on accder ssh ssh.ufr-info-p6.jussieu.fr,on peut voir les gens qui sont entraine de connecter :
21202829@ssh:~$ finger
Login     Name        Tty      Idle  Login Time   Office     Office Phone
21104817  CONSTANCE   pts/4      47  Oct 16 18:46 (176.186.195.18)
21202829  YUXIANG     pts/2          Oct 16 18:29 (46.193.67.26)
21317623  SAMIA       pts/1      22  Oct 16 18:26 (81.65.149.218)
yellas                pts/12   3:42  Oct 16 14:05 (132.227.78.120)

Question 11
last -da > nouvelle_trace.log

Question 12
./traces.sh nouvelle_trace.log

Exercice 3
Question 1
21202829@ssh:~$ ps -eF
UID          PID    PPID  C    SZ   RSS PSR STIME TTY          TIME CMD
root           1       0  0 42367 13952   1 oct.14 ?       00:00:06 /sbin/init
root           2       0  0     0     0   5 oct.14 ?       00:00:00 [kthreadd]
root           3       2  0     0     0   0 oct.14 ?       00:00:00 [rcu_gp]
root           4       2  0     0     0   0 oct.14 ?       00:00:00 [rcu_par_gp]
root           5       2  0     0     0   0 oct.14 ?       00:00:00 [slub_flushwq]
root           6       2  0     0     0   0 oct.14 ?       00:00:00 [netns]
root           8       2  0     0     0   0 oct.14 ?       00:00:00 [kworker/0:0H-events_highpri]
root          10       2  0     0     0   0 oct.14 ?       00:00:00 [mm_percpu_wq]
root          11       2  0     0     0   0 oct.14 ?       00:00:00 [rcu_tasks_kthread]
root          12       2  0     0     0   0 oct.14 ?       00:00:00 [rcu_tasks_rude_kthread]
root          13       2  0     0     0   0 oct.14 ?       00:00:00 [rcu_tasks_trace_kthread]
root          14       2  0     0     0   0 oct.14 ?       00:00:00 [ksoftirqd/0]
root          15       2  0     0     0   0 oct.14 ?       00:00:08 [rcu_preempt]
root          16       2  0     0     0   0 oct.14 ?       00:00:00 [migration/0]
root          18       2  0     0     0   0 oct.14 ?       00:00:00 [cpuhp/0]
root          19       2  0     0     0   1 oct.14 ?       00:00:00 [cpuhp/1]
root          20       2  0     0     0   1 oct.14 ?       00:00:01 [migration/1]
root          21       2  0     0     0   1 oct.14 ?       00:00:00 [ksoftirqd/1]
root          23       2  0     0     0   1 oct.14 ?       00:00:00 [kworker/1:0H-events_highpri]
root          24       2  0     0     0   2 oct.14 ?       00:00:00 [cpuhp/2]
root          25       2  0     0     0   2 oct.14 ?       00:00:01 [migration/2]
root          26       2  0     0     0   2 oct.14 ?       00:00:00 [ksoftirqd/2]
root          28       2  0     0     0   2 oct.14 ?       00:00:00 [kworker/2:0H-events_highpri]
root          29       2  0     0     0   3 oct.14 ?       00:00:00 [cpuhp/3]
root          30       2  0     0     0   3 oct.14 ?       00:00:01 [migration/3]
root          31       2  0     0     0   3 oct.14 ?       00:00:00 [ksoftirqd/3]
root          33       2  0     0     0   3 oct.14 ?       00:00:00 [kworker/3:0H-events_highpri]
root          34       2  0     0     0   4 oct.14 ?       00:00:00 [cpuhp/4]
root          35       2  0     0     0   4 oct.14 ?       00:00:01 [migration/4]
root          36       2  0     0     0   4 oct.14 ?       00:00:14 [ksoftirqd/4]
root          38       2  0     0     0   4 oct.14 ?       00:00:00 [kworker/4:0H-events_highpri]
root          39       2  0     0     0   5 oct.14 ?       00:00:00 [cpuhp/5]
root          40       2  0     0     0   5 oct.14 ?       00:00:01 [migration/5]
root          41       2  0     0     0   5 oct.14 ?       00:00:00 [ksoftirqd/5]
root          43       2  0     0     0   5 oct.14 ?       00:00:00 [kworker/5:0H-events_highpri]
root          44       2  0     0     0   6 oct.14 ?       00:00:00 [cpuhp/6]
root          45       2  0     0     0   6 oct.14 ?       00:00:01 [migration/6]
root          46       2  0     0     0   6 oct.14 ?       00:00:00 [ksoftirqd/6]
root          48       2  0     0     0   6 oct.14 ?       00:00:00 [kworker/6:0H-events_highpri]
root          49       2  0     0     0   7 oct.14 ?       00:00:00 [cpuhp/7]
root          50       2  0     0     0   7 oct.14 ?       00:00:01 [migration/7]
root          51       2  0     0     0   7 oct.14 ?       00:00:00 [ksoftirqd/7]
root          53       2  0     0     0   7 oct.14 ?       00:00:00 [kworker/7:0H-events_highpri]
root          62       2  0     0     0   1 oct.14 ?       00:00:00 [kdevtmpfs]
root          63       2  0     0     0   4 oct.14 ?       00:00:00 [inet_frag_wq]
root          64       2  0     0     0   4 oct.14 ?       00:00:00 [kauditd]
root          65       2  0     0     0   6 oct.14 ?       00:00:00 [khungtaskd]
root          66       2  0     0     0   1 oct.14 ?       00:00:00 [oom_reaper]
root          67       2  0     0     0   3 oct.14 ?       00:00:00 [writeback]
root          68       2  0     0     0   1 oct.14 ?       00:00:05 [kcompactd0]
root          69       2  0     0     0   3 oct.14 ?       00:00:00 [ksmd]
root          70       2  0     0     0   3 oct.14 ?       00:00:02 [khugepaged]
root          71       2  0     0     0   3 oct.14 ?       00:00:00 [kintegrityd]
root          72       2  0     0     0   0 oct.14 ?       00:00:00 [kblockd]
root          73       2  0     0     0   0 oct.14 ?       00:00:00 [blkcg_punt_bio]
root          75       2  0     0     0   4 oct.14 ?       00:00:00 [tpm_dev_wq]
root          76       2  0     0     0   4 oct.14 ?       00:00:00 [edac-poller]
root          77       2  0     0     0   4 oct.14 ?       00:00:00 [devfreq_wq]
root          78       2  0     0     0   0 oct.14 ?       00:00:00 [kworker/0:1H-kblockd]
root          79       2  0     0     0   3 oct.14 ?       00:00:00 [kswapd0]
root          87       2  0     0     0   7 oct.14 ?       00:00:00 [kthrotld]
root          89       2  0     0     0   7 oct.14 ?       00:00:00 [acpi_thermal_pm]
root          90       2  0     0     0   4 oct.14 ?       00:00:00 [mld]
root          91       2  0     0     0   1 oct.14 ?       00:00:00 [kworker/1:1H-kblockd]
root          92       2  0     0     0   4 oct.14 ?       00:00:00 [ipv6_addrconf]
root          97       2  0     0     0   4 oct.14 ?       00:00:00 [kstrp]
root         102       2  0     0     0   4 oct.14 ?       00:00:00 [zswap-shrink]
root         103       2  0     0     0   4 oct.14 ?       00:00:00 [kworker/u17:0]
root         157       2  0     0     0   4 oct.14 ?       00:00:00 [kworker/4:1H-kblockd]
root         158       2  0     0     0   7 oct.14 ?       00:00:00 [kworker/7:1H-kblockd]
root         159       2  0     0     0   6 oct.14 ?       00:00:00 [kworker/6:1H-kblockd]
root         160       2  0     0     0   5 oct.14 ?       00:00:00 [kworker/5:1H-kblockd]
root         161       2  0     0     0   2 oct.14 ?       00:00:00 [kworker/2:1H-kblockd]
root         162       2  0     0     0   3 oct.14 ?       00:00:00 [kworker/3:1H-kblockd]
root         177       2  0     0     0   2 oct.14 ?       00:00:00 [ata_sff]
root         178       2  0     0     0   6 oct.14 ?       00:00:00 [scsi_eh_0]
root         179       2  0     0     0   3 oct.14 ?       00:00:00 [scsi_tmf_0]
root         180       2  0     0     0   0 oct.14 ?       00:00:00 [scsi_eh_1]
root         181       2  0     0     0   3 oct.14 ?       00:00:00 [scsi_tmf_1]
root         183       2  0     0     0   3 oct.14 ?       00:00:00 [scsi_eh_2]
root         184       2  0     0     0   1 oct.14 ?       00:00:00 [scsi_tmf_2]
root         234       2  0     0     0   3 oct.14 ?       00:00:00 [jbd2/sda8-8]
root         235       2  0     0     0   6 oct.14 ?       00:00:00 [ext4-rsv-conver]
root         279       1  0 114915 191336 5 oct.14 ?       00:00:21 /lib/systemd/systemd-journald
root         318       1  0  6761  6964   2 oct.14 ?       00:00:01 /lib/systemd/systemd-udevd
root         443       2  0     0     0   7 oct.14 ?       00:00:00 [jbd2/sda1-8]
root         444       2  0     0     0   4 oct.14 ?       00:00:00 [ext4-rsv-conver]
root         447       2  0     0     0   7 oct.14 ?       00:00:00 [jbd2/sda7-8]
root         448       2  0     0     0   7 oct.14 ?       00:00:00 [ext4-rsv-conver]
root         450       2  0     0     0   4 oct.14 ?       00:00:02 [jbd2/sda6-8]
root         451       2  0     0     0   2 oct.14 ?       00:00:00 [ext4-rsv-conver]
_rpc         585       1  0  1969  3836   1 oct.14 ?       00:00:00 /sbin/rpcbind -f -w
systemd+     586       1  0 22512  6612   7 oct.14 ?       00:00:00 /lib/systemd/systemd-timesyncd
root         588       2  0     0     0   6 oct.14 ?       00:00:00 [rpciod]
root         589       2  0     0     0   6 oct.14 ?       00:00:00 [xprtiod]
root         591       1  0 65524 16084   0 oct.14 ?       00:00:05 /usr/libexec/accounts-daemon
root         592       1  0   625  1092   7 oct.14 ?       00:00:00 /usr/sbin/acpid
avahi        596       1  0  5880 11260   5 oct.14 ?       00:00:01 avahi-daemon: running [ssh-2.local]
root         598       1  0  1652  2652   5 oct.14 ?       00:00:01 /usr/sbin/cron -f
message+     599       1  0  6302 12280   4 oct.14 ?       00:00:01 /usr/bin/dbus-daemon --system --address=systemd: -polkitd      602       1  0 81568 19520   6 oct.14 ?       00:00:00 /usr/lib/polkit-1/polkitd --no-debug
root         606       1  0 55450  6672   7 oct.14 ?       00:00:05 /usr/sbin/rsyslogd -n -iNONE
root         608       1  0  4824  7716   3 oct.14 ?       00:00:00 /lib/systemd/systemd-logind
root         609       1  0 98438 17544   3 oct.14 ?       00:00:00 /usr/libexec/udisks2/udisksd
daemon       619       1  0   895  1188   1 oct.14 ?       00:00:00 /usr/sbin/atd -f
root         628       1  0 165399 12428  7 oct.14 ?       00:00:06 /usr/sbin/nscd
root         630       1  0   618    92   3 oct.14 ?       00:00:07 /usr/sbin/atopacctd
avahi        658     596  0  5699  1696   3 oct.14 ?       00:00:00 avahi-daemon: chroot helper
root         664       1  0 65405 22244   0 oct.14 ?       00:00:02 /usr/sbin/NetworkManager --no-daemon
root         666       1  0  4130  5800   5 oct.14 ?       00:00:00 /sbin/wpa_supplicant -u -s -O DIR=/run/wpa_supplicroot         677       1  0 60894 12012   1 oct.14 ?       00:00:00 /usr/sbin/ModemManager
root         701       1  0 101435 27036  1 oct.14 ?       00:01:13 /usr/bin/python3 /usr/bin/fail2ban-server -xf starroot         745       1  0  4511  9324   4 oct.14 ?       00:00:03 sshd: /usr/sbin/sshd -D [listener] 0 of 10-100 staroot         806       1  0 106746 9048   6 oct.14 ?       00:00:04 /usr/sbin/automount --pid-file /var/run/autofs.pidroot        1086       1  0 62372 11184   6 oct.14 ?       00:00:00 /usr/sbin/gdm3
Debian-+    1094       1  0 11007 16540   4 oct.14 ?       00:00:14 /usr/sbin/exim4 -bd -q30m
root        1104    1086  0 45277 13332   1 oct.14 ?       00:00:00 gdm-session-worker [pam/gdm-launch-environment]
Debian-+    1116       1  0  4767 10704   6 oct.14 ?       00:00:01 /lib/systemd/systemd --user
Debian-+    1117    1116  0 46266  3960   5 oct.14 ?       00:00:00 (sd-pam)
Debian-+    1139    1116  0 10781  8340   1 oct.14 ?       00:00:00 /usr/bin/pipewire
Debian-+    1142    1116  0  7334  8852   3 oct.14 ?       00:00:00 /usr/bin/pipewire-pulse
Debian-+    1143    1104  0 39865  8228   0 oct.14 tty1    00:00:00 /usr/libexec/gdm-wayland-session dbus-run-session
Debian-+    1145    1143  0  4177  3680   7 oct.14 tty1    00:00:00 dbus-daemon --print-address 3 --session
rtkit       1146       1  0  6302  3592   6 oct.14 ?       00:00:01 /usr/libexec/rtkit-daemon
Debian-+    1221    1143  0  1565  1564   1 oct.14 tty1    00:00:00 dbus-run-session -- gnome-session --autostart /usrDebian-+    1222    1221  0  4292  4684   5 oct.14 tty1    00:00:00 dbus-daemon --nofork --print-address 4 --session
Debian-+    1223    1221  0 130195 20296  3 oct.14 tty1    00:00:00 /usr/libexec/gnome-session-binary --autostart /usrDebian-+    1258    1223  0 1258391 215556 2 oct.14 tty1   00:03:09 /usr/bin/gnome-shell
Debian-+    1334       1  0 77858  9536   7 oct.14 tty1    00:00:00 /usr/libexec/at-spi-bus-launcher
Debian-+    1339    1334  0  4177  4112   3 oct.14 tty1    00:00:00 /usr/bin/dbus-daemon --config-file=/usr/share/defaDebian-+    1349    1258  0 57817 65836   2 oct.14 tty1    00:00:00 /usr/bin/Xwayland :1024 -rootless -noreset -accessDebian-+    1365       1  0 59253  9908   2 oct.14 tty1    00:00:00 /usr/libexec/xdg-permission-store
root        1371       1  0 58475  8428   7 oct.14 ?       00:00:00 /usr/libexec/upowerd
Debian-+    1386       1  0 712592 31044  7 oct.14 tty1    00:00:00 /usr/bin/gjs /usr/share/gnome-shell/org.gnome.ShelDebian-+    1388       1  0 41078  9416   5 oct.14 tty1    00:00:00 /usr/libexec/at-spi2-registryd --use-gnome-sessionDebian-+    1390    1223  0 115932 12800  2 oct.14 tty1    00:00:00 /usr/libexec/gsd-sharing
Debian-+    1393    1223  0 84950 27292   3 oct.14 tty1    00:00:00 /usr/libexec/gsd-wacom
Debian-+    1394    1223  0 85224 25624   3 oct.14 tty1    00:00:00 /usr/libexec/gsd-color
Debian-+    1395    1223  0 84781 24692   5 oct.14 tty1    00:00:00 /usr/libexec/gsd-keyboard
Debian-+    1396    1223  0 62484 13592   5 oct.14 tty1    00:00:00 /usr/libexec/gsd-print-notifications
Debian-+    1397    1223  0 113748 10536  6 oct.14 tty1    00:00:00 /usr/libexec/gsd-rfkill
Debian-+    1398    1223  0 78146 12072   1 oct.14 tty1    00:00:00 /usr/libexec/gsd-smartcard
Debian-+    1399    1223  0 88960 14176   3 oct.14 tty1    00:00:00 /usr/libexec/gsd-datetime
Debian-+    1408    1223  0 167886 33928  2 oct.14 tty1    00:00:00 /usr/libexec/gsd-media-keys
Debian-+    1409    1223  0 58352  6916   1 oct.14 tty1    00:00:00 /usr/libexec/gsd-screensaver-proxy
Debian-+    1410    1223  0 79993 13800   1 oct.14 tty1    00:00:00 /usr/libexec/gsd-sound
colord      1411       1  0 61210 15232   5 oct.14 ?       00:00:00 /usr/libexec/colord
Debian-+    1413    1223  0 76989 10912   0 oct.14 tty1    00:00:00 /usr/libexec/gsd-a11y-settings
Debian-+    1414    1223  0 95853 10020   3 oct.14 tty1    00:00:04 /usr/libexec/gsd-housekeeping
Debian-+    1415    1223  0 113402 30748  0 oct.14 tty1    00:00:00 /usr/libexec/gsd-power
Debian-+    1500       1  0 85534 17760   2 oct.14 tty1    00:00:00 /usr/libexec/gsd-printer
Debian-+    1585       1  0 698256 27664  4 oct.14 tty1    00:00:00 /usr/bin/gjs /usr/share/gnome-shell/org.gnome.Screstatd       1692       1  0  2759  2676   1 oct.14 ?       00:00:00 /sbin/rpc.statd
root        1710       2  0     0     0   3 oct.14 ?       00:00:00 [nfsiod]
root        1716       2  0     0     0   2 oct.14 ?       00:00:00 [lockd]
root        4315       2  0     0     0   1 oct.14 ?       00:00:03 [kworker/1:0-events]
21201059   35407       1  0  2232  1748   7 oct.15 ?       00:00:11 nc ppti-14-502-01 22
21201059   36337       1  0  2232  1912   6 oct.15 ?       00:00:00 nc ppti-14-502-02 22
21201059   36404       1  0  2232  1744   6 oct.15 ?       00:00:00 nc ppti-14-502-03 22
21201059   36467       1  0  2232  1904   7 oct.15 ?       00:00:06 nc ppti-14-502-10 22
21201059   36868       1  0  2232  1888   5 oct.15 ?       00:00:01 nc ppti-14-502-05 22
21201059   36961       1  0  2232  1964   4 oct.15 ?       00:00:00 nc ppti-14-502-06 22
root       38336       2  0     0     0   0 oct.15 ?       00:00:02 [kworker/0:2-events]
root       45247       1  0  6404 24472   2 00:00 ?        00:00:05 /usr/bin/atop -w /var/log/atop/atop_20231016 600
root       45267       1  0  8993  9096   4 00:00 ?        00:00:00 /usr/sbin/cupsd -l
root       45269       1  0 44694 15084   3 00:00 ?        00:00:00 /usr/sbin/cups-browsed
root       50405       2  0     0     0   2 05:23 ?        00:00:00 [kworker/2:2-events]
21201059   53383       1  0  2232  1908   6 08:24 ?        00:00:12 nc ppti-14-502-01 22
21201059   54661       1  0  2232  1776   6 09:32 ?        00:00:00 nc ppti-14-502-10 22
21201059   54727       1  0  2232  1888   5 09:34 ?        00:00:00 nc ppti-14-502-05 22
root       59013       2  0     0     0   7 13:09 ?        00:00:00 [kworker/7:3-events]
root       60734     745  0  9034 16076   1 14:04 ?        00:00:00 sshd: yellas [priv]
yellas     60743       1  0  4773 10840   4 14:05 ?        00:00:00 /lib/systemd/systemd --user
yellas     60744   60743  0 47549  5520   6 14:05 ?        00:00:00 (sd-pam)
yellas     60759   60743  0 10782  8552   4 14:05 ?        00:00:00 /usr/bin/pipewire
yellas     60763   60743  0  7301  8724   3 14:05 ?        00:00:00 /usr/bin/pipewire-pulse
yellas     60771   60734  0  9102  7836   3 14:05 ?        00:00:01 sshd: yellas@pts/12
yellas     60787   60771  0  2833  5644   2 14:05 pts/12   00:00:00 -bash
root       68583       2  0     0     0   3 15:41 ?        00:00:02 [kworker/3:2-mm_percpu_wq]
yellas    104075   60787  0  5780  8764   6 15:57 pts/12   00:00:00 ssh -X ppti-14-501-01
root      105169       2  0     0     0   5 16:56 ?        00:00:00 [kworker/5:0-events]
root      115495       2  0     0     0   2 18:09 ?        00:00:00 [kworker/2:0]
root      115573       2  0     0     0   6 18:14 ?        00:00:00 [kworker/6:1-events]
root      115701     745  0  9047 15736   5 18:26 ?        00:00:00 sshd: 21317623 [priv]
21317623  115708  115701  0  9112  7684   7 18:26 ?        00:00:00 sshd: 21317623@pts/1
21317623  115709  115708  0  2734  5232   0 18:26 pts/1    00:00:00 -bash
root      115743     745  0  9046 15744   6 18:29 ?        00:00:00 sshd: 21202829 [priv]
21202829  115749  115743  0  9111  7640   6 18:29 ?        00:00:00 sshd: 21202829@pts/2
21202829  115750  115749  0  2767  5440   3 18:29 pts/2    00:00:00 -bash
21317623  115848  115709  0  5813  8820   6 18:35 pts/1    00:00:00 ssh -X ppti-24-302-09
root      115873     745  0  9045 15824   3 18:37 ?        00:00:00 sshd: 21104817 [priv]
21104817  115879  115873  0  9110  7676   5 18:37 ?        00:00:02 sshd: 21104817
root      115988       2  0     0     0   4 18:39 ?        00:00:00 [kworker/4:1-events]
root      116043       2  0     0     0   6 18:43 ?        00:00:00 [kworker/6:0]
root      116119     745  0  9047 15764   6 18:45 ?        00:00:00 sshd: 21104817 [priv]
21104817  116130  116119  0  9112  7736   1 18:46 ?        00:00:00 sshd: 21104817@pts/4
21104817  116131  116130  0  2804  5588   0 18:46 pts/4    00:00:00 -bash
root      116166       2  0     0     0   1 18:47 ?        00:00:00 [kworker/1:1]
root      116267       2  0     0     0   5 18:51 ?        00:00:00 [kworker/5:2-mm_percpu_wq]
root      116593     745  0  9046 15784   3 19:01 ?        00:00:00 sshd: 28712181 [priv]
28712181  116611  116593  0  9111  7588   0 19:01 ?        00:00:00 sshd: 28712181
root      116830       2  0     0     0   5 19:10 ?        00:00:00 [kworker/u16:0-xprtiod]
root      116921       2  0     0     0   0 19:16 ?        00:00:00 [kworker/0:0]
root      117083       2  0     0     0   4 19:24 ?        00:00:00 [kworker/u16:1-events_unbound]
root      117191       2  0     0     0   4 19:27 ?        00:00:00 [kworker/4:0-events_freezable]
root      117284       2  0     0     0   3 19:34 ?        00:00:00 [kworker/3:0-events]
root      117415       2  0     0     0   7 19:39 ?        00:00:00 [kworker/7:1]
root      117517       2  0     0     0   0 19:46 ?        00:00:00 [kworker/u16:2-events_unbound]
21202829  117602  115750  0  3430  4400   5 19:52 pts/2    00:00:00 ps -eF

Question 2
Pour comparer la longueur des manuels des commandes ps et mkdir, on peut utiliser la commande man suivie du nom de la commande :

Pour ps :
man ps | wc -w

Pour mkdir :
man mkdir | wc -w

Cela nous donnera le nombre de mots dans le manuel de chaque commande. Comparez les deux résultats pour noter la différence de complexité entre les deux commandes.

Il s'affiche:
21202829@ssh:~$ man ps | wc -w
7366
21202829@ssh:~$ man mkdir | wc -w
310

Question 3:
cd /
cat /proc/1222/stat
1222 (dbus-daemon) S 1221 1143 1143 1025 1143 4194304 720 267 0 0 4 5 0 0 20 0 1 0 3347 17580032 1171 18446744073709551615 1 1 0 0 0 0 0 0 16385 0 0 0 17 5 0 0 0 0 0 0 0 0 0 0 0 0 0

Pour trouver le PPID de 1222:
21202829@ssh:/$ cat /proc/1222/stat | cut -d ' ' -f 4
1221

Pour trouver le nom du processus correspondant à ce PPID:
21202829@ssh:/$ cat /proc/1222/stat | cut -d ' ' -f 2
(dbus-daemon)

Question 4:
Il me reste 10 min ... Pouvez vous m'aider à trouver mes ancêtres.
Pour vous aider voici mon pid 118395

Question 5:
#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Erreur : Aucun PID fourni en paramètre."
    exit 1
fi

pid=$1

if ! ps -p $pid > /dev/null; then
    echo "Erreur : Le PID $pid n'existe pas."
    exit 1
fi

while [ $pid -ne 1 ]; do
    echo $pid
    stat_file="/proc/$pid/stat"
    ppid=$(cut -d ' ' -f 4 $stat_file)
    pid=$ppid
done

echo 1

Question 6
systemd(1)─┬─ModemManager(677)─┬─{ModemManager}(704)
           │                   └─{ModemManager}(742)
           ├─NetworkManager(664)─┬─{NetworkManager}(697)
           │                     └─{NetworkManager}(698)
           ├─accounts-daemon(591)─┬─{accounts-daemon}(642)
           │                      └─{accounts-daemon}(662)
           ├─acpid(592)
           ├─at-spi-bus-laun(1334)─┬─dbus-daemon(1339)
           │                       ├─{at-spi-bus-laun}(1335)
           │                       ├─{at-spi-bus-laun}(1336)
           │                       └─{at-spi-bus-laun}(1338)
           ├─at-spi2-registr(1388)─┬─{at-spi2-registr}(1419)
           │                       └─{at-spi2-registr}(1420)
           ├─atd(619)
           ├─atop(45247)
           ├─atopacctd(630)
           ├─automount(806)─┬─{automount}(807)
           │                ├─{automount}(808)
           │                └─{automount}(942)
           ├─avahi-daemon(596)───avahi-daemon(658)
           ├─colord(1411)─┬─{colord}(1512)
           │              └─{colord}(1514)
           ├─cron(598)
           ├─cups-browsed(45269)─┬─{cups-browsed}(45270)
           │                     └─{cups-browsed}(45271)
           ├─cupsd(45267)
           ├─dbus-daemon(599)
           ├─exim4(1094)
           ├─fail2ban-server(701)─┬─{fail2ban-server}(1097)
           │                      ├─{fail2ban-server}(1110)
           │                      ├─{fail2ban-server}(1111)
           │                      └─{fail2ban-server}(117438)
           ├─gdm3(1086)─┬─gdm-session-wor(1104)─┬─gdm-wayland-ses(1143)─┬─dbus-daemon(1145)
           │            │                       │                       ├─dbus-run-sessio(1221)─┬─dbus-daemon(1222)
           │            │                       │                       │                       └─gnome-session-b(122+           │            │                       │                       ├─{gdm-wayland-ses}(1144)
           │            │                       │                       └─{gdm-wayland-ses}(1217)
           │            │                       ├─{gdm-session-wor}(1106)
           │            │                       └─{gdm-session-wor}(1108)
           │            ├─{gdm3}(1099)
           │            └─{gdm3}(1100)
           ├─gjs(1386)─┬─{gjs}(1400)
           │           ├─{gjs}(1401)
           │           ├─{gjs}(1402)
           │           ├─{gjs}(1403)
           │           ├─{gjs}(1404)
           │           ├─{gjs}(1405)
           │           ├─{gjs}(1406)
           │           ├─{gjs}(1407)
           │           ├─{gjs}(1416)
           │           └─{gjs}(1417)
           ├─gjs(1585)─┬─{gjs}(1588)
           │           ├─{gjs}(1589)
           │           ├─{gjs}(1590)
           │           ├─{gjs}(1591)
           │           ├─{gjs}(1592)
           │           ├─{gjs}(1593)
           │           ├─{gjs}(1594)
           │           ├─{gjs}(1595)
           │           ├─{gjs}(1596)
           │           └─{gjs}(1597)
           ├─gsd-printer(1500)─┬─{gsd-printer}(1508)
           │                   └─{gsd-printer}(1509)
           ├─nc(35407)
           ├─nc(36337)
           ├─nc(36404)
           ├─nc(36467)
           ├─nc(36868)
           ├─nc(36961)
           ├─nc(53383)
           ├─nc(54661)
           ├─nc(54727)
           ├─nscd(628)─┬─{nscd}(647)
           │           ├─{nscd}(648)
           │           ├─{nscd}(649)
           │           ├─{nscd}(650)
           │           ├─{nscd}(651)
           │           ├─{nscd}(652)
           │           ├─{nscd}(653)
           │           └─{nscd}(654)
           ├─polkitd(602)─┬─{polkitd}(661)
           │              └─{polkitd}(665)
           ├─rpc.statd(1692)
           ├─rpcbind(585)
           ├─rsyslogd(606)─┬─{rsyslogd}(638)
           │               ├─{rsyslogd}(639)
           │               └─{rsyslogd}(640)
           ├─rtkit-daemon(1146)─┬─{rtkit-daemon}(1148)
           │                    └─{rtkit-daemon}(1149)
           ├─sshd(745)─┬─sshd(60734)───sshd(60771)───bash(60787)───ssh(104075)
           │           ├─sshd(115701)───sshd(115708)───bash(115709)───ssh(115848)
           │           ├─sshd(115743)───sshd(115749)───bash(115750)───pstree(118540)
           │           ├─sshd(115873)───sshd(115879)
           │           ├─sshd(116119)───sshd(116130)───bash(116131)
           │           ├─sshd(116593)───sshd(116611)
           │           ├─sshd(117899)───sshd(117915)───bash(117925)───ssh(118110)
           │           ├─sshd(117916)───sshd(117922)───sftp-server(117923)
           │           ├─sshd(118090)───sshd(118105)
           │           ├─sshd(118259)───sshd(118265)───bash(118266)
           │           └─sshd(118536)
           ├─systemd(1116)─┬─(sd-pam)(1117)
           │               ├─pipewire(1139)───{pipewire}(1173)
           │               └─pipewire-pulse(1142)───{pipewire-pulse}(1177)
           ├─systemd(60743)─┬─(sd-pam)(60744)
           │                ├─pipewire(60759)───{pipewire}(60781)
           │                └─pipewire-pulse(60763)───{pipewire-pulse}(60783)
           ├─systemd-journal(279)
           ├─systemd-logind(608)
           ├─systemd-timesyn(586)───{systemd-timesyn}(590)
           ├─systemd-udevd(318)
           ├─udisksd(609)─┬─{udisksd}(643)
           │              ├─{udisksd}(663)
           │              ├─{udisksd}(678)
           │              └─{udisksd}(691)
           ├─upowerd(1371)─┬─{upowerd}(1373)
           │               └─{upowerd}(1374)
           ├─wpa_supplicant(666)
           └─xdg-permission-(1365)─┬─{xdg-permission-}(1366)
                                   └─{xdg-permission-}(1368)