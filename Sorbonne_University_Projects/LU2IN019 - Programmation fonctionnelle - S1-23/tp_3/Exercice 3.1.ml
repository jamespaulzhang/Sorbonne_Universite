let rec is_in (e : 'a) (l : 'a list) : bool = 
  match l with
  | [] -> false
  | h :: t -> if e = h then true else is_in e t ;;
  
(is_in 4 []);;
(is_in 3 [1;3;2]);;
(is_in 4 [1;3;2]);;

let add_elem (e : 'a) (l : 'a list) : 'a list =
  if l = [] then [e]
  else if is_in e l then l else e :: l ;;

(add_elem 4 [1;3;2]);;
(add_elem 4 [1;3;4;2]);;
(add_elem 4 []);;