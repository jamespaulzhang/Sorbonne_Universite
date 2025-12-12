.data
p: .word 5

.text
main:
addiu $29,$29,-4
lui $4,0x1001
lw $4,0($4)
jal fact

ori $4,$2,0
ori $2,$0,1
syscall

addiu $29,$29,4
ori $2,$0,10
syscall

fact:
addiu $29,$29,-12 #na = 1;nv = 1;nr = 1:$31
sw $31,8($29)
sw $4,12($29)
bne $4,$0,else
ori $2,$0,1
j epiloque

else:
addiu $4,$4,-1
jal fact
lw $4,12($29)
multu $4,$2
mflo $2

epiloque:
lw $31,8($29)
addiu $29,$29,12
jr $31
