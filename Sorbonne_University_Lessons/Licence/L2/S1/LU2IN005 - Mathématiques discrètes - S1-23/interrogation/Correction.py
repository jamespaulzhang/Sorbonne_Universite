def asserteq(a,b):
	assert(a==b)
	return

## Test successeur
auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") #Correspond à l'automate "auto"
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

asserteq(auto_t1.succ({s0, s2}, 'b'),{s1}) 
asserteq(auto_t1.succ({s0}, 'a'),{s0})
asserteq(auto_t1.succ({s0, s1}, 'a'),{s0, s2})

#test sur 3 états
asserteq(auto_t1.succ({s0,s1,s2}, 'b'),{s1, s2})


#tests sur un automate non déterministe
auto_t2 = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
#auto_t2.show(1.2) #debug
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, False)
s3 = State(3, False, True)
asserteq(auto_t2.succ({s0}, 'a'),{s0, s1})
asserteq(auto_t2.succ({s2,s3}, 'a'),{s3})
asserteq(auto_t2.succ({s0}, 'b'),{s0})

auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") 
auto_t2 = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
#auto_t2.show(1.2) #debug
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, False)
s3 = State(3, False, True)

#test sur une lettre ne faisant pas parti de l'alphabet
asserteq(auto_t1.succ({s0, s1}, 'c'), set())


#Test sur l'automate sans transition d'unique état 0
seul=State(0,True,True)
solitaire=Automate(set(),{seul})
asserteq(solitaire.succ({seul}, 'c'), set())

#Tests cas vides :
asserteq(auto_t1.succ(set(),'a'),set())
auto_vide=Automate(set())
asserteq(auto_vide.succ({s0},'a'),set())

### Test accepte
auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") #Correspond à l'automate "auto"

asserteq(auto_t1.accepte('aa'),False)
asserteq(auto_t1.accepte('ab'),False)
asserteq(auto_t1.accepte('aba'),True)
asserteq(auto_t1.accepte('aab'), False)
asserteq(auto_t1.accepte('abba'),False)
asserteq(auto_t1.accepte('abaaa'),False)
asserteq(auto_t1.accepte(''),False)
asserteq(auto_t1.accepte('bb'),True)
asserteq(auto_t1.accepte('abbbbbbbb'),True)
asserteq(auto_t1.accepte('abbbbbbb'),False)
asserteq(auto_t1.accepte('ccccc'),False)

#tests sur un automate non déterministe
auto_t2 = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
#auto_t2.show(1.2) #debug

asserteq(auto_t2.accepte('baab'), False)
asserteq(auto_t2.accepte('baaab'), True)
asserteq(auto_t2.accepte('baaaaaaaa'), True)
asserteq(auto_t2.accepte('bbbbbbbb'), False)

auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") #Correspond à l'automate "auto"

#test sur un automate à 2 états finaux
s0 = State(0, True, True)
s1 = State(1, False, True)
deux_f=Automate({Transition(s0,'a',s0),Transition(s0,'b',s1)},{s0,s1})
asserteq(deux_f.accepte('a'), True)

#test sur un automate sans états final ni initial
s3=State(0,False,False)
auto_if = Automate({Transition(s3,'a',s3)},{s3})
asserteq(auto_if.accepte('a'),False)
asserteq(auto_if.accepte(''),False)

#test sur un automate sans état final
s4=State(0,True,False)
auto_f = Automate({Transition(s4,'a',s4)},{s4})
asserteq(auto_f.accepte('a'),False)
asserteq(auto_f.accepte(''),False)

#test sur un automate sans état initial
s5 = State(0,False,True)
auto_i=Automate({Transition(s5,'a',s5)},{s5})
asserteq(auto_i.accepte('a'),False)
asserteq(auto_i.accepte(''),False)

#test sur un etat initial et final
s6=State(0,True,True)
auto_all=Automate(set(),{s6})
asserteq(auto_all.accepte(''),True)

#tests cas vides :
auto_vide=Automate(set())
asserteq(auto_vide.accepte('a'),False)
asserteq(auto_vide.accepte(''),False)


### Test est_complet

auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") #Correspond à l'automate "auto"

asserteq(auto_t1.estComplet({'a', 'b'}),True)

asserteq(auto_t1.accepte('ab'),False)

#test sur un alphabet plus petit
asserteq(auto_t1.estComplet({'a'}),True)
#test sur un alphabet plus grand
asserteq(auto_t1.estComplet({'a','b','c'}),False)


#tests sur un automate non déterministe
auto_t2 = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
#auto_t2.show(1.2) #debug
asserteq(auto_t2.estComplet({'a'}),True)
asserteq(auto_t2.estComplet({'a','b'}),False)


#test cas vides

auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") #Correspond à l'automate "auto" 
asserteq(auto_t1.estComplet(set()),True)

auto_vide=Automate(set())
asserteq(auto_vide.estComplet('a'),True)

s6=State(0,True,True)
auto_all=Automate(set(),{s6})
asserteq(auto_all.estComplet('a'),False)



### Test est_deterministe

s0 = State(0, True, False)
s1 = State(1, False, False)
t = Transition(s1, 'b', s0)
auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt")#Correspond à l'automate "auto"

asserteq(auto_t1.estDeterministe(), True)

auto_t1.addTransition(t)

asserteq(auto_t1.estDeterministe(), False)

auto_t1.removeTransition(t)


#tests sur 2 automates non déterministes

auto_t2 = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
#auto_t2.show(1.2) #debug
asserteq(auto_t2.estDeterministe(), False)

auto_t3 = Automate.creationAutomate("ExemplesAutomates/auto_cours_p21.txt")
#auto_t3.show(1.2) #debug
asserteq(auto_t3.estDeterministe(), False)

#test sur un automate avec 2 états initiaux
seul1=State(0,True,True)
seul2=State(1,True,True)

solitaire=Automate(set(),{seul1,seul2})
asserteq(solitaire.estDeterministe(), False)



auto_vide=Automate(set())
asserteq(auto_vide.estDeterministe(),False)

s6=State(0,True,True)
auto_all=Automate(set(),{s6})
asserteq(auto_all.estDeterministe(),True)

s7=State(0,False,True)
auto_all=Automate({Transition(s7,'a',s7)},{s7})
asserteq(auto_all.estDeterministe(),False)

### Test completeAutomate
auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt")#Correspond à l'automate "auto"



asserteq(auto_t1.estComplet({'a', 'b', 'c'}), False)
auto_t1_c =auto_t1.completeAutomate({'a', 'b', 'c'})
asserteq(auto_t1_c.estComplet({'a', 'b','c'}),True)


#tests sur un automate non déterministe
auto_t3 = Automate.creationAutomate("ExemplesAutomates/auto_cours_p21.txt")

#auto_t3.show(1.2) #debug



auto_comp1 = auto_t3.completeAutomate({'a', 'b'})
asserteq(auto_comp1.estComplet({'a', 'b'}), True)


#vérifie que l'état puit soit ni final ni inital
ens=auto_comp1.succElem(State(2,False,False),'b')
for s in ens:
    asserteq(s.init,False)
    asserteq(s.fin,False)
    

auto_comp2 = auto_t3.completeAutomate({'a'})
asserteq(auto_comp2.estComplet({'a'}), True)

auto_comp3 = auto_t3.completeAutomate({'a','b','c'})
asserteq(auto_comp3.estComplet({'a','b','c'}), True)
       
### Test newl_label
auto_t1 = Automate.creationAutomate("ExemplesAutomates/auto2.txt") #Correspond à l'automate "auto"

asserteq(newLabel(auto_t1.allStates),'{0,1,2}')


s0 = State(0, True, False)
s1 = State(1, False, False)
asserteq(newLabel(auto_t1.allStates),newLabel(auto_t1.allStates))

s0 = State(0, True, False,"B")
s1 = State(1, False, False,"C")
asserteq(newLabel({s0,s1}),'{B,C}')
asserteq(newLabel({s0}),'{B}') 


### Tests determinisation
auto_t2 = Automate.creationAutomate("ExemplesAutomates/exempleAutomate.txt")
asserteq(auto_t2.estDeterministe(), False)
auto_det = auto_t2.determinisation()
asserteq(auto_det.estDeterministe(), True)

       
asserteq(auto_det.accepte('baab'), False)
asserteq(auto_det.accepte('baaab'), True)
asserteq(auto_det.accepte('baaaaaaaa'), True)
asserteq(auto_det.accepte('bbbbbbbb'), False)
asserteq(auto_det.accepte('aaaba'), True)



auto_t3 = Automate.creationAutomate("ExemplesAutomates/auto_cours_p21.txt")
    
auto_det = auto_t3.determinisation()
asserteq(auto_det.estDeterministe(), True)
#auto_det.show(1.7) #debug
#7
asserteq(auto_det.accepte('ab'), False)
asserteq(auto_det.accepte('baaab'), False)
asserteq(auto_det.accepte('baaaaaaaa'), False)
asserteq(auto_det.accepte('bbbbbbbb'), False)
asserteq(auto_det.accepte('bbbbbbbbaba'), True)
asserteq(auto_det.accepte('aba'), True)
asserteq(auto_det.accepte('bbbbbbbbaba'), True)
