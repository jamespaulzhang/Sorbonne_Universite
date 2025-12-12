let rec less_divider (i : int) (n : int) : int =
  if i = n then 0 
  else if n mod i = 0 then i 
  else less_divider (i+1) n ;;

(less_divider 2 19) ;;
(less_divider 5 21) ;;
(less_divider 7 21) ;;
(less_divider 9 21) ;;

let prime (n : int) : bool =
  if n = 1 then false
  else less_divider 2 n = 0 ;;

(prime 1) ;;
(prime 21) ;;
(prime 19) ;;

let rec next_prime (n : int) : int = 
  if prime n then n
  else next_prime (n+1) ;;

(next_prime 0) ;;
(next_prime 15) ;;
(next_prime 19) ;;

  let nth_prime n =
    let rec find_prime count current =
      if count = n then current
      else
        let next = current + 1 in
        if prime next then find_prime (count + 1) next
        else find_prime count next
    in
    find_prime 0 2 ;;
  
(nth_prime 0) ;;
(nth_prime 1) ;;
(nth_prime 2) ;;
(nth_prime 3) ;;
(nth_prime 12) ;;

