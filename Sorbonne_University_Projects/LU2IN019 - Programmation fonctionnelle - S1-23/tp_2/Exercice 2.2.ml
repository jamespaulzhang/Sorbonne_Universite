(* La methode avec utiliser la fonction range_inter *)
let rec genere_list (n : int) : int list =
  let rec range_inter(a : int) (b : int): int list =
  if a > b then []
  else a :: (range_inter (a + 1) b) 
  in
  range_inter 2 n ;;

(genere_list 1);;
(genere_list 4);; 

(* La methode sans utiliser la fonction range_inter *)
let rec genere_list_2 (n : int) : int list =
  if n < 2 then []
  else genere_list_2(n - 1) @ [n] ;;

(genere_list_2 1);;
(genere_list_2 4);; 

(* Sans recursive *)
let elimine (l : int list) (n : int) : int list =
  List.filter (fun (x : int) : bool -> not (x mod n = 0)) l ;;

(elimine [1; 2; 3; 4; 5; 6] 3);;

(* Avec recursive *)
let rec elimine_rec (l : int list) (n : int) : int list =
  match l with
  | [] -> []
  | h :: t -> if h mod n = 0 then elimine_rec t n else h :: elimine_rec t n ;;

(elimine_rec [1; 2; 3; 4; 5; 6] 3);;

let ecreme (l : int list) : int list =
  let rec aux (acc : int list) = function
    | [] -> List.rev acc
    | x :: xs ->
      let is_multiple (y : int) : bool = x mod y = 0 in
      if not (List.exists is_multiple acc) then aux (x :: acc) xs else aux acc xs
  in
  aux [] l ;;

(ecreme [2; 3; 4; 5; 6; 7; 8; 9; 10; 11; 12]);;

let crible (n : int) : int list =
  let l = genere_list n in ecreme l ;;

(crible 1);;
(crible 20);;