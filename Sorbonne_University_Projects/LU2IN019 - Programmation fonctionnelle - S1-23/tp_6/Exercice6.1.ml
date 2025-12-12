type int_set = 
  | N of int_set * int_set
  | E of bool;;

type bin = int list;;

let ex = N(N(E true,E true),N(E false,E true));;

exception Not_prefect;;
exception No_fit;;

let rec hauteur_equilibre (t: int_set) : int = 
  match t with
  | E _ -> 0
  | N(g,d) -> let x = hauteur_equilibre g in
              let y = hauteur_equilibre d in
              if x <> y then raise Not_prefect
              else x + 1;;
      
(hauteur_equilibre ex);;
(* (hauteur_equilibre (N(N(E true,E true),E false)));; *) 

let rec int_to_bin (i : int) : int list =
  if i = 0 || i = 1 then [i]
  else (i mod 2) :: int_to_bin (i / 2) ;;

let mem (x : int) (t : int_set) : bool = 
  let rec doit (b : bin) (t : int_set) : bool = 
    match b,t with
    | [] , E b -> b
    | [] , N (g,d) -> doit [] g
    | a :: b, N (g,d) -> if a = 0 then doit b g else doit b d
    | _ -> false
  in
  doit (int_to_bin x) t;;

(mem 2 ex);;
(mem 1 ex);;

let insert_exn(t : int_set) (x : int) : int_set = 
  let rec doit (t : int_set) (b : bin) =
    match t,b with
    | E b , [] -> E true
    | N(g,d) , [] -> N(doit g [] , d)
    | N(g,d) , a :: b -> if a = 0 then N(doit g [a] , d) else N(g, doit d b)
    | _ -> raise No_fit
  in
  doit t (int_to_bin x);;

(insert_exn ex 1);;
(* (insert_exn ex 25);; *)