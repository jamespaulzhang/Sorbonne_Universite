let rec is_in (e : 'a) (l : 'a list) : bool = 
  match l with
  | [] -> false
  | h :: t -> if e = h then true else is_in e t ;;

let rec is_subset_rec (l1 : 'a list) (l2 : 'a list) : bool =
  match l1 with
  | [] -> true
  | h :: t -> if is_in h l2 then is_subset_rec t l2 else false ;;

(is_subset_rec [4;2] [0;2;4;6]);;
(is_subset_rec [] [0;2;4;6]);;
(is_subset_rec [2;3;4] [0;2;4;6]);;
(is_subset_rec [4;2;0;6] [0;2;4;6]);;

let is_subset (l1 : 'a list) (l2 : 'a list) : bool = 
  List.for_all (fun e -> is_in e l2) l1  ;;

(is_subset_rec [4;2] [0;2;4;6]);;
(is_subset_rec [] [0;2;4;6]);;
(is_subset_rec [2;3;4] [0;2;4;6]);;
(is_subset_rec [4;2;0;6] [0;2;4;6]);;
let eq_set (l1 : 'a list) (l2 : 'a list) : bool =
  if List.for_all (fun e -> is_in e l2) l1  && List.for_all (fun e -> is_in e l1) l2 then true else false ;;

(eq_set [4;2] [0;2;4;6]);;
(eq_set [4;2;6;0] [0;2;5;6]);;
(eq_set [4;2;6;0] [0;2;4;6]);;
(eq_set [] []);;