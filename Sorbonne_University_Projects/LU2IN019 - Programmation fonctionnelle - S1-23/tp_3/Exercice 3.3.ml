let rec is_in (e : 'a) (l : 'a list) : bool = 
  match l with
  | [] -> false
  | h :: t -> if e = h then true else is_in e t ;;

let rec intersection_rec (l1 : 'a list) (l2 : 'a list) : 'a list =
  match l1 with 
  | [] -> []
  | h :: t -> if is_in h l2 then h :: intersection_rec t l2 else intersection_rec t l2 ;;

(intersection_rec [] [3;5;4;6]);;
(intersection_rec [1;2;3;4] []);;
(intersection_rec [1;2;3;4] [3;5;4;6]);;

let intersection (l1: 'a list) (l2 : 'a list) :  'a list = 
  List.filter (fun e -> is_in e l1) l2 ;;

(intersection_rec [] [3;5;4;6]);;
(intersection_rec [1;2;3;4] []);;
(intersection_rec [1;2;3;4] [3;5;4;6]);;