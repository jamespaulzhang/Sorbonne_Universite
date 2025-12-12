type 'a btree = Empty | Node of 'a * ('a btree) * ('a btree);;

let sag (t : 'a btree) : 'a btree = match t with
    Empty -> raise (Invalid_argument "sag")
  | Node (e,g,d) -> g;;

let sad (t : 'a btree) : 'a btree = match t with
    Empty -> raise (Invalid_argument "sad")
  | Node (e,g,d) -> g;;

let t = Node (2, Node (1, Empty, Empty),Node (2, Node (3, Empty, Empty), Empty));;

(sad (sag t));;


(sag (sag (sad t)));;


(sag (sad (sad t)));;


(sag (sag (sag t)));;


(sag (sad t));;


(sag (sag t));;


(sad (sag (sad t)));;


(sad (sag (sag t)));;