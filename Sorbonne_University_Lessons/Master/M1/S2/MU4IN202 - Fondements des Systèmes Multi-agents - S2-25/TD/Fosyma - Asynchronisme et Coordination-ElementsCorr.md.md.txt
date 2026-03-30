Fosyma - TD7 : Asynchronisme et Coordination
===
Éléments de correction
## 2. Consensus et généraux Byzantins

### 1. Description de l'algorithme (n>3f+1) : cas synchrone

__Cas P(f=0)__ :	
 1. Le capitaine $C_0$ envoie une valeur $v$ à tous les capitaines
 2. Pour tout  $C_i$ (avec $i\neq 0$),  $v_{C_i}= v$ ou $Err$

__Cas P(f):__ _(avec n>3f>0 et donc f>0)_
 1. Le capitaine $C_0$ envoie une valeur $v$ à tous les capitaines 
 2. Pour tout  $C_i$ (avec $i\neq 0$)
     a. $v_{c_i}^{c_0}= v$ ou $Err$ (si délai de garde dépassé)
     b. Appel récursif à P(f-1) en se comportant comme $C_0$ et diffusant pour les n-2 capitaines restants
 3. Pour tout  $C_j$ (avec $i\neq j$),$v_{c_j}^{c_i}(P(f-1))= val$ ou $Err$
     avec $val=majorité(v_{c_0},..,v_{c_{n-1}})$ ou Err
 
 
 #### Q2. Combien de messages échangés ?
 

| Etape | nb messages envoyés | 
| -------- | -------- | 
| P(0)     | n-1      | 
| P(1)     | (n-1) * (n-2)      | 
| P(f)     | (n-1) * (n-2) * .. * (n-(f+1))      | 
| P(f)     | $O(n^f)$|


### 2.  Diffusion asynchrone avec (n>3f+1)

1. Plus de possibilité de distinguer un messagé intercepté d'un message ne retard.
2. Pseudo Code :
 - Phase d'initialisation :  L'emetteur diffuse son message <echo,v>
 - Phase de réception : Chaque récepteur rediffuse la valeur reçue à tous par un echo
    - Si un procéssus a reçu plus de (n+f)/2 messages <echo,v> ou plus de f messages <ready,v>, alors ils transmet <ready,v> à tous.
    - Si un procesus a reçu 2f+1 messages <ready,v> avec le même v alors il décide que la valeur $v$ est bien la valeur diffusée. 
    
3. Exemple pour n=4,f=1



|Tour | 0 | 1(f) | 2 |3 |
|-| -------- | -------- | -------- |-------- |
|1| ↑E,1       |      |     | |
|2| ↑E,1       | ↓E,1     | ↓E,1     |↓E,1 |
|3|        | ↑E,0 (3) et ↑E,1 (0,2)     | ↑E,1     |↑E,1 |
|**4**| ↓**3E,1**       |      | ↓**3E,1**     |↓2E,1 et ↓1E,0|
|5| ↑R,1       |      | ↑R,1     ||
|**6**| ↓2R,1       |      | ↓2R,1     |↓2E,1 et ↓1E,0 et ↓**2R,1**|
|7|        |      |      |↑R,1|
|**8**| ↓**3R,1**       |      | ↓**3R,1**     |↓2E,1 et ↓1E,0 et ↓**3R,1**|
|9| décide,1      |      |décide,1     |décide,1 |

4. Si l'émetteur initial est fiable, la décision prise est celle de l'émetteur. 
Si l'émetteur n'est pas fiable.. et sans tenir compte de l'asynchronisme, la décision sera celle de la majorité, elle-même conditionnée par la valeur majoritairement envoyée par l'émetteur initial.



