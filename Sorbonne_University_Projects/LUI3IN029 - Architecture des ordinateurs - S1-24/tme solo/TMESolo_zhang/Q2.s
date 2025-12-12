#Yuxiang ZHANG 21202829
.data
cle:
.asciiz "vigenere"
msg_crypte:
.space 256 #char[256]
msg_decrypte:
.space 256  #char[256]

.text
#prologue
addiu $29,$29,-8 #na = 2,nv =0,nr =0
lui $4,0x1001
addiu $4,$4,12 #@msg_crypte
ori $5,$0,256 #max 256 octets pour saisir
ori $2,$0,8
syscall

#printf msg_crypte
lui $4,0x1001
addiu $4,$4,12 #@msg_crypte
ori $2,$0,4
syscall

#@msg_crypte
lui $4,0x1001
addiu $4,$4,12

#@msg_decrypte
lui $5,0x1001
addiu $5,$5,268
jal decrypter

#printf msg_decrypte
lui $4,0x1001
addiu $4,$4,268
ori $2,$0,4
syscall

#epilogue
addiu $29,$29,8
ori $2,$0,10
syscall

decrypter:
#prologue
addiu $29,$29,-20 #na = 0,nr = 1($31),nv = 4
sw $31,16($29)

xor $8,$8,$8 #i = 0
xor $9,$9,$9 #j = 0
ori $10,$0,256 #256
for:
slt $11,$8,$10 #$11 = 1 si i < 256
beq $11,$0,fin_for
or $12,$0,$4 #@a_decrypter
addu $12,$12,$8 #@a_decrypter[i]
lbu $13,0($12) # c = a_decrypter[i]
sb $13,12($29) #save c dans la pile
#if1
lbu $13,12($29) #load c
bne $13,$0,fin_if_1
or $14,$0,$5 #@decrypte
addu $14,$14,$8 #@decrypte[i]
sb $0,0($14) #decrypte[i] = '\0'
ori $8,$0,256
fin_if_1:
#else
#if2
lui $15,0x1001 #@cle
addu $15,$15,$9 #@cle[j]
lbu $15,0($15) #cle[j]
bne $15,$0,fin_if_2
xor $9,$9,$9 #j = 0
addiu $15,$15,-0x61 #cle[j] - 0x61
sw $15,8($29) #save delta
fin_if_2:
#if 3
lb $15,8($29) #delta
sub $15,$13,$15 #c-delta
slti $15,$15,0x61 #$15 = 1 si c - delta < 0x61
beq $15,$0,fin_if_3
addiu $13,$13,26 #c = c+26
sb $13,12($29) #save c dans la pile
fin_if_3:
lb $15,8($29) #delta
sub $15,$13,$15 #c-delta
or $14,$0,$5 #@decrypte
addu $14,$14,$8 #@decrypte[i]
sb $15,0($14) # decrypte[i] = c-delta
addiu $9,$9,1
j for
fin_for:
#epilogue
ori $2,$0,0 #return 0
lw $31,16($29)
addiu $29,$29,20
jr $31




