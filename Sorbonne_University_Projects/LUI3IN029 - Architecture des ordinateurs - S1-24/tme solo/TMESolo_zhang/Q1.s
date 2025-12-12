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
ori $2,$0,10
syscall




