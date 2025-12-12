let rec factorielle (n : int) : int =
  if n = 0 then 1 else n * (factorielle (n-1)) ;;

assert((factorielle 0) = 1) ;;
assert((factorielle 3) = 6) ;;