.data

.text
ori $9,$0,84
ori $10,$0,10

div $9,$10
mflo $11
mfhi $12
ori $2,$0,1
or $4,$0,$11
syscall

ori $2,$0,11
ori $4,$0,0x0A #'/n'
syscall

ori $2,$0,1
or $4,$0,$12
syscall

ori $2,$0,10
syscall
