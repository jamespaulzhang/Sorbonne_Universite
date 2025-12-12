.data
s: .space 20
ch_ok: .asciiz "bien parenthésé\n"
ch_nok: .asciiz "mal parenthésé\n"

.text
main:
	addiu $29,$29,-12
	lui $4,0x1001
	ori $5,$0,19
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
	j ajout
	ok: 
	lui $4,0x1001
	ori $4,$4,20
	ori $2,$0,4
	syscall
	ajout:
	lui $4,0x1001
	xor $5,$5,$5
	jal bon_parenthesage_rec
	sw $2, 4($29) # seulement si pas optimise
	lw $2, 4($29) # seulement si pas optimise	
	beq $2,$0,ok2
	lui $4,0x1001
	ori $4,$4,37
	ori $2,$0,4
	syscall
	j fin
	ok2: 
	lui $4,0x1001
	ori $4,$4,20
	ori $2,$0,4
	syscall
	
	fin:
	addiu $29,$29,12
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
		
bon_parenthesage_rec:
	# nr = 0 + $31, nv = 1, na = 2
	addiu $29, $29, -16
	sw $31, 12($29)
	add $9, $4, $5 # @ch[i]
	lbu $9, 0($9)
	bne $9, $0, not_zero
	xor $2, $2, $2 # cas ch[index] == 00
	j bpr_epilogue
	not_zero:
	sw $4, 16($29) # sauvegarde param
	sw $5, 20($29)
	addi $5, $5, 1 # index + 1
	jal bon_parenthesage_rec
	sw $2, 8($29) # sauvegarde resultat dans d, peut etre optimisé
	blez $2, d_neg
	j bpr_epilogue # cas d positif => fin
	d_neg:
	lw $4, 16($29)
	lw $5, 20($29)
	add $8, $4, $5
	lbu $8, 0($8) # ch[index]
	ori $10, $0, 0x29
	bne $8, $10, not_par_close
	addi $2, $2, -1
	j bpr_epilogue
	not_par_close:
	ori $10, $0, 0x28
	bne $8, $10, bpr_epilogue
	addi $2, $2, 1
	bpr_epilogue:
	lw $31, 12($29)
	addiu $29, $29, 16
	jr $31
