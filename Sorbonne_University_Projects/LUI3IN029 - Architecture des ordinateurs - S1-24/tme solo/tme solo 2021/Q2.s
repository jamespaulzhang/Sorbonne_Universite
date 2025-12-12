.data
user_num:
.align 2 
.space 4
tab_chiffre:
.align 2
.space 40

.text
#pilogue
addiu $29,$29,-12 #nv =1 ,na = 2,nr = 0
#scanf user_num
ori $2,$0,5
syscall
lui $8,0x1001
sw $2,0($8)
lw $4,0($8) #arg1 de occ_num_chiffre
lui $5,0x1001
ori $5,$5,4 #arg1 = @tab_chiffre
jal occ_num_chiffre
sw $2,8($29)

#affichage
lui $4,0x1001
ori $4,$4,4 #arg1 de la fonction affichage
jal affichage

#printf num_ch
lw $4,8($29)
ori $2,$0,1
syscall
#epilogue
addiu $29,$29,12
ori $2,$10,10
syscall

occ_num_chiffre:
addiu $29,$29,-16 #nv = 3,na = 0,nr ($31) = 1
sw $31,12($29)

ori $2,$0,1 #nb_c = 1
or $8,$0,$4 # q = n
ori $9,$0,0 # r = 0
ori $10,$0,10 # 10
# while
loop:
slt $11,$8,$10 # $11 = 1 si q < 10
bne $11,$0,fin_loop # si q < 10 fin_loop
div $8,$10
mfhi $9 #$9 = r 
mflo $8 #$8 = q
sll $12,$9,2 #r*4
addu $12,$12,$5 #@t[r]
lw $13,0($12) #t[r]
addiu $13,$13,1 #t[r]+1
sw $13,0($12) # t[r] = t[r]+1
addiu $2,$2,1
j loop
fin_loop:
sll $12,$8,2 #r*4
addu $12,$12,$5 #@t[r]
lw $13,0($12) #t[r]
addiu $13,$13,1 #t[r]+1
sw $13,0($12) # t[r] = t[r]+1
lw $31,12($29)
addiu $29,$29,16
jr $31

affichage:
addiu $29,$29,-16 #na = 0 ,nv = 1, nr = 3
sw $31,12($29)
sw $16,4($29)
sw $17,8($29)

#for
xor $16,$16,$16 #j = 0
or $17,$0,$4 #@tab
for:
slti $10,$16,10
beq $10,$0,fin_for
#print j
or $4,$0,$16
ori $2,$0,1
syscall
#print ':'
ori $4,$0,':'
ori $2,$0,11
syscall
#print t[j]
sll $8,$16,2 #j*4
addu $8,$8,$17 #@t[j]
lw $4,0($8) #t[j]
ori $2,$0,1
syscall
#print ';'
ori $4,$0,';'
ori $2,$0,11
syscall
addiu $16,$16,1
j for
fin_for:
#print '\n'
ori $4,$0,'\n'
ori $2,$0,11
syscall
lw $16,4($29)
lw $17,8($29)
lw $31,12($29)
addiu $29,$29,16
jr $31