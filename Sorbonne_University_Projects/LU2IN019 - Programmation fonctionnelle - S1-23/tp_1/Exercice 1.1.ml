let rec sum_chiffres(n : int) : int = 
  if n = 0 then 0 else n - 10*(n/10) + sum_chiffres(n/10) ;;

sum_chiffres(125);; 
let rec nb_chiffres(n : int) : int =
  if n/10 = 0 then 1 else 1 + nb_chiffres(n/10) ;;

nb_chiffres(125);;