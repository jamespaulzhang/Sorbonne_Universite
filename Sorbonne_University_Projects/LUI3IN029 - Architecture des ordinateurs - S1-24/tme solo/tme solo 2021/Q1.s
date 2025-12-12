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

#printf num_ch
ori $2,$0,1
lw $4,8($29)
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