type 'a btree = 
  | Empty 
  | Node of ('a * 'a btree * 'a btree);;

let rec lt_btree (t : 'a btree) (x : 'a) : bool =
  match t with
  | Empty -> true
  | Node(a, sag, sad) -> (a < x) && (lt_btree sag x && lt_btree sad x) ;;

assert((lt_btree (Node(2,Node(4,Empty,Empty),Empty)) 5) = true);;
assert((lt_btree Empty 5) = true);;
assert((lt_btree (Node(4,Node(6,Empty,Empty),Empty)) 5) = false);;

let rec ge_btree (t: 'a btree) (x: 'a) : bool =
  match t with
  | Empty -> true
  | Node(a, sag, sad) -> (a >= x) && (ge_btree sag x && ge_btree sad x) ;;

assert((ge_btree (Node(4,Node(5,Empty,Empty),Empty)) 4) = true);;
assert((ge_btree Empty 5) = true);;
assert((ge_btree (Node(4,Node(3,Empty,Empty),Empty)) 4) = false);;

let rec is_abr(bt: 'a btree) : bool =
  match bt with
  | Empty -> true
  | Node(a, sag, sad) -> ((lt_btree sag a && ge_btree sad a)) && ((is_abr sag) && (is_abr sad));;

assert((is_abr Empty) = true);;

let rec mem (bt : 'a btree) (x : 'a) : bool =
  match bt with
  | Empty -> false
  | Node(a, sag, sad) -> (a = x) || (mem sag x || mem sad x);;

assert((mem (Node (5,Empty,Empty)) 5) = true);;


  