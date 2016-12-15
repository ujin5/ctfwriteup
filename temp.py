import socket
import struct
import telnetlib

def q(x):
  return struct.pack('<I',x);
def recv_until(s,string):
  r = ""
  while not r.endswith(string):
    tmp = s.recv(1)
    if not tmp:break;
    r += tmp
  return r
def interact(s):
  print "INTERACT"
  t = telnetlib.Telnet()
  t.sock = s
  t.interact()
s = socket.create_connection(['pwnable.kr',9001])
