type 'a btree = Empty | Node of 'a * ('a btree) * ('a btree);;


let rec f (x : 'a) (t : 'a btree) : bool = match t with
   Empty -> false
 | Node (e,_,y) -> e=x || f x y;;

let t = Node (1, Node (2, Empty, Empty), Node (3, Empty, Empty));;
(f 3 t);;

Node (3, Node (3, Empty, Empty), Node (1, Empty, Empty))


Node (2, Node (3, Empty, Empty), Node (1, Empty, Empty))


Node (2, Node (1, Empty, Empty),Node (2, Node (3, Empty, Empty), Empty))


Node (1, Node (3, Empty, Empty), Empty)