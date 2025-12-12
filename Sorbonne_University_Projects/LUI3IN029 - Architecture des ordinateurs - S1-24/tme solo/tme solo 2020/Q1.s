.data
s: .space 20
ch_ok: .asciiz "bien parenthésé\n"
ch_nok: .asciiz "mal parenthésé\n"

.text
main:
	addiu $29,$29,-8
	lui $4,0x1001
	ori $5,$0,20
	ori $2,$0,8
	syscall
	
	lui $4,0x1001
	ori $2,$0,4
	syscall
	
	lui $4,0x1001
	jal bon_parenthesage
	sw $2, 4($29) # seulement si pas optimise
	lw $2, 4($29) # seulement si pas optimise	
	beq $2,$0,ok
	lui $4,0x1001
	ori $4,$4,37
	ori $2,$0,4
	syscall
	j fin
	ok: 
	lui $4,0x1001
	ori $4,$4,20
	ori $2,$0,4
	syscall
	fin:
	addiu $29,$29,8
	ori $2,$0,10
	syscall
	
bon_parenthesage:
	addiu $29,$29,-12
	sw $31,8($29)
	xor $2,$2,$2
	xor $8,$8,$8
	ori $10,$0,0x28
	ori $11,$0,0x29
	loop:
		addu $12,$4,$8
		lbu $9,0($12)
		beq $9,$0,end
		bne $9,$10,suite1
		addiu $2,$2,1
		j suite3
		suite1:
		bne $9,$11,suite3
		addiu $2,$2,-1
		suite3:
		bltz $2,end
		addiu $8,$8,1
		j loop
	end:
		lw $31,8($29)
		addiu $29,$29,12
		jr $31	