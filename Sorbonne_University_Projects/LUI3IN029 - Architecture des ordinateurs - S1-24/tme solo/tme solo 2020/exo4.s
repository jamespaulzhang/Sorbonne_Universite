.data
tab1: .word 23,4,5,-1
tab2: .word 2,345,56,23,45,-1

.text
addiu $29,$29,-4
lui $4,0x1001
jal nb_elem

ori $4,$2,0
ori $2,$0,1
syscall

ori $4,$0,0xA
ori $2,$0,11
syscall
lui $4,0x1001
ori $4,$4,16
jal nb_elem

ori $4,$2,0
ori $2,$0,1
syscall

addiu $29,$29,4
ori $2,$0,10
syscall

nb_elem:
addiu $29,$29,-12
sw $31,8($29)
xor $2,$2,$2
loop:
lw $6,0($4)
bltz $6,fin
addiu $2,$2,1
addiu $4,$4,4
j loop
fin:
lw $31,8($29)
addiu $29,$29,12
jr $31
