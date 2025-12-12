let rec bin_to_int (i : int list) : int =
  match i with
  | [] -> raise (Invalid_argument "empty list")
  | [h] -> h
  | h :: t -> h + 2 * bin_to_int t;;

bin_to_int [];;

bin_to_int [1];;

bin_to_int [0; 1; 1];;

bin_to_int [0; 1; 1; 0];;

bin_to_int [0; 1; 1; 0; 0];;

bin_to_int [1; 1; 0; 1; 0; 1];;

let rec int_to_bin (i : int) : int list =
  if i = 0 || i = 1 then [i]
  else (i mod 2) :: int_to_bin (i / 2) ;;
  
int_to_bin 0;;
int_to_bin 1;;
int_to_bin 6;;
int_to_bin 43;;

let rec comp_bin (l : int list) (n : int) : int list =
  if n < List.length l then raise (Invalid_argument "comp_bin")
  else if n = List.length l then l
  else comp_bin (l @ [0]) n ;;

comp_bin [1; 0] 2;;
comp_bin [1; 0] 4;;
comp_bin [0; 1; 1] 2;;