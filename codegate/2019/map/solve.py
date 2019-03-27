from pwn import *
import pyte

import re
#context.log_level = 'debug'
screen = pyte.Screen(90,45)
stream = pyte.Stream(screen)

MY_BLOCKS_RE = re.compile(r'\[(\d)\]\s*(\d+)\s')
r = remote('54.180.100.218', 20489)
screen_result = ''

def get_result():
    return escape(screen_result)

def recv_end(s=0, skip_first=False):
    global screen_result
    if not skip_first:
        r.recvuntil('*******\n')
        r.recvuntil('*****\n')
        r.recvuntil('[40m')

    d = r.recvuntil('*******\n')
    d += r.recvuntil('*****\n')
    d += r.recvuntil('[40m')
    screen_result = d
    if s:
        return escape(d)
    return d

def escape(s):
    stream.feed(s)
    return '\n'.join(screen.display)

def move(d, num=1, multi=False):
    s = ''
    if d == '^':
        for i in xrange(num):
            r.sendline('u')
            s = recv_end()
    elif d == '<':
        for i in xrange(num):
            r.sendline('h')
            s = recv_end()
    elif d == '>':
        for i in xrange(num):
            r.sendline('k')
            s = recv_end()
    elif d == 'v':
        for i in xrange(num):
            r.sendline('j')
            s = recv_end()
    else:
        raise 'Direction'
    return s

def moves(t=[]):
    for tt in t:
        move(tt[0],tt[1])

def get_block():
    r.sendline('g')
    recv_end()

def go_room2():
    moves([('>',13),('v', 10),('>', 30),('^', 10),('>', 10),('^', 5), ('>', 4)])

def go_room3():
    moves([('>',3),('^',2),('>',45), ('^',1),('>',3),('v',3),('>',6)])

def go_room4():
    moves([('>',5),('v',1),('>',4),('^',2),('>',44), ('v',1),('>',3)])

def find_block(x, y):
    s = get_result()
    arr = s.split('[E]')[1].split('=== BLOCK')[0].split('|<')[1:]
    arr = map(lambda x: list(x), arr)
    for y in xrange(y):
        for x in xrange(x):
            if arr[y][x] in 'e':
                return x,y 
    return (None,None)

def collect_block():
    x, y = find_block(12, 4)
    if x is not None:
        moves([('>', x), ('v', y)])
        get_block()
        moves([('<', x), ('^', y)])
    moves([('<', 1), ('>',1)])

def collect_blocks():
    blocks = []
    while True:
        blocks = get_my_blocks()
        collect_block()
        print get_result()
        if len(filter(lambda x: x != None, blocks)) == 6:
            break
    return blocks
    
def get_my_blocks():
    s = get_result()
    parsed_blocks = MY_BLOCKS_RE.findall(s)
    blocks = [None for x in xrange(6)]
    for idx, value in parsed_blocks:
        blocks[int(idx)] = int(value)
    return blocks

def merge_block(idx1, idx2):
    r.sendline('m')
    
    r.recvuntil('[1st Block] : ')
    r.sendline(str(idx1))
    r.recvuntil('[2nd Block] : ')
    r.sendline(str(idx2))
    r.recvuntil('********')
    recv_end(skip_first=True)
    move('<',1)

def get_mergable_blocks(blocks):
    for i in xrange(len(blocks)):
        for j in xrange(len(blocks)):
            if i == j or not blocks[j]:
                continue
            if blocks[i] == blocks[j]:
                return i, j
    return  None, None

def merge():
    moves([('<',3), ('^',2),('>',3),('^',2),('<',5)])
    while True:
        blocks = get_my_blocks()
        blocks = filter(lambda x: x != None, blocks)
        if len(set(blocks)) == len(blocks):
            break
        blocks = get_my_blocks()
        idx1, idx2 = get_mergable_blocks(blocks)
        merge_block(idx1,idx2)
        print get_result()
    moves([('>', 5),('v',2),('<',3),('v',2),('>',3)])

r.recv()
r.sendline('')
r.recv()
r.sendline('')
r.recv()
r.sendline('ASDF')
r.recv()
go_room2()
go_room3()
go_room4()
while True:
    blocks = get_my_blocks()
    collect_blocks()
    merge()
    if blocks[0] == 1024:
        break
print get_result()
