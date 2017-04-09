import struct
import telnetlib
import socket
import hexdump
import datetime
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
def p32(x):
  return struct.pack('<I',x)
def p64(x):
  return struct.pack('<Q',x)
def u32(x):
  return struct.unpack('<I',x)[0]
def u64(x):
  return struct.unpack('<Q',x)[0]
def host_tuple(target):
  return type(target) == list and len(target) == 2 and isinstance(target[1], int) and target[1] >= 0 and target[1] < 65536
def log(string):
  logger('OKGREEN','+',string)
def logger(mode,mark,string):
  if mode == 'OKBLUE':
    print '['+bcolors.OKBLUE+mark+bcolors.ENDC+']'+string
  if mode == 'OKGREEN':
    print '['+bcolors.OKGREEN+mark+bcolors.ENDC+']'+string
  if mode == 'HEADER':
    print '['+bcolors.HEADER+mark+bcolors.ENDC+']'+string
  if mode == 'WARNING':
    print '['+bcolors.WARNING+mark+bcolors.ENDC+']'+string
  if mode == 'FAIL':
    print '['+bcolors.FAIL+mark+bcolors.ENDC+']'+string
class IOI(object):
  def __init__(self,target):
    self.again_IOI()
    self.target = target
    if not host_tuple(target):
      raise Exception("IS NOT SOCKET TUPLE")
    self.sock = socket.create_connection(target)
    logger('OKBLUE','+'," Connect %s : %d"%(target[0],target[1]))
  def write(self,dat):
    self.sock.send(dat)
    return len(dat)
  def read(self,size=1024):
    return self.sock.recv(size)
  def read_until(self,string):
    r = ''
    while not r.endswith(string):
      tmp = self.read(1)
      if not tmp:break;
      r += tmp
    return r
  def interact(self):
    logger('OKBLUE','+',' INTERACT')
    self.telnet = telnetlib.Telnet()
    self.telnet.sock = self.sock
    self.telnet.interact()
  def again_IOI(self):
    start_time = datetime.datetime(2021,5,4,12,00)
    seconds = (start_time - datetime.datetime.today())
    self.IOI = seconds
    logger('HEADER','!',' Again IOI, '+"%d days"%seconds.days)
