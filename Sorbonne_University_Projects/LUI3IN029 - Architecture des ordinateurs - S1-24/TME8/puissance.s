.data
p: .word 3
m: .word 5

.text
main:
addiu $29,$29,-8
lui $4,0x1001
lw $4,0($4)
lui $5,0x1001
addiu $5,$5,4
lw $5,0($5)
jal puissance

ori $4,$2,0
ori $2,$0,1
syscall

addiu $29,$29,8
ori $2,$0,10
syscall

puissance:
addiu $29,$29,-16 #na=2;nv=1;nr=1
sw $31,12($29)
sw $4,16($29)
sw $5,20($29)

bne $5,$0,if2
ori $2,$0,1
j epiloque

if2:
ori $8,$0,1
bne $5,$8,else
ori $2,$4,0
j epiloque

else:
ori $9,$0,2
div $5,$9
mflo $5
jal puissance

#ori $8,$0,1
lw $5,20($29)
andi $5,$5,0x01
bne $5,$8,else2
multu $2,$2
mflo $2
multu $2,$4
mflo $2
j epiloque

else2:
multu $2,$2
mflo $2

epiloque:
lw $31,12($29)
addiu $29,$29,16
jr $31