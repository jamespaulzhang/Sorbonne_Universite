let rec is_in (e : 'a) (l : 'a list) : bool = 
  match l with
  | [] -> false
  | h :: t -> if e = h then true else is_in e t ;;

let add_elem (e : 'a) (l : 'a list) : 'a list =
  if l = [] then [e]
  else if is_in e l then l else e :: l ;;

let rec union_rec (l1 : 'a list) (l2 : 'a list) : 'a list =
  let l3 = [] in
  match (l1,l3) with
  | ([],_) -> l2
  | (_,_) -> l3
  | (h :: t,x :: y) -> if  h = x then union_rec l1 l2 else h :: l3;; 

(union_rec [1;2;3;4] [3;4;5;6]);;
(union_rec [] [3;5;4;6]);;