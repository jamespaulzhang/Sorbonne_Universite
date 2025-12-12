.data
n: .word 15
m: .word -1
l: .word 124

.text
addiu $29,$29,-24
lui $8,0x1001
lw $4,0($8)
lw $5,4($8)
ori $6,$0,5
jal moyenne3
ori $16,$2,0
or $4,$16,$0
ori $2,$0,1
syscall

lui $8,0x1001
lw $4,4($8)
lw $5,8($8)
addiu $6,$4,5
ori $7,$0,12
ori $10,$0,35
sw $10,16($29)
jal moyenne5
ori $16,$2,0
or $4,$16,$0
ori $2,$0,1
syscall

addiu $29,$29,24
ori $2,$0,10
syscall

moyenne3:
addiu $29,$29,-12
sw $31,8($29)
sw $16,4($29)
addu $8,$4,$5
addu $16,$8,$6
ori $9,$0,3
div $16,$9
mflo $2
lw $16,4($29)
lw $31,8($29)
addiu $29,$29,12
jr $31

moyenne5:
addiu $29,$29,-12
sw $31,8($29)
sw $16,4($29)
lw $10,28($29)
addu $8,$4,$5
addu $8,$8,$6
addu $8,$8,$7
addu $16,$8,$10
ori $9,$0,5
div $16,$9
mflo $2
lw $16,4($29)
lw $31,8($29)
addiu $29,$29,12
jr $31