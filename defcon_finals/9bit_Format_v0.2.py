import sys

class Formatter:
    def __init__(self, data):
        self.data = self.to9bit_list(data)

    def print_all(self, align=0x18):
        count = 0
        for data in self.data:
            if count%align == 0:
                sys.stdout.write('\n[%6s] ' % hex(count))
            sys.stdout.write('%6s ' % hex(data))
            count +=1

    def toHex(self, offset, size):
        return map(lambda x : hex(x), self.data[offset:offset+size])
        
    def to9bit_list(self, data):
        
        result = []
        byte_len = len(data)/9
        
        for idx in range(byte_len):
            d = data[idx*9:(idx+1)*9]
            for i in range(8):
                a = (ord(d[i])<<(i+1))&0b111111111
                a = a | (ord(d[i+1])>>(7-i))
                result.append(a)            
        return result

    def find(self, search_list, sindex=0):

        start_byte = search_list[0]
        find_idx = 0

        while find_idx != -1:
            try:
                find_idx = self.data.index(start_byte, sindex)
            except ValueError:
                return -1
                
            sindex = find_idx + 1
            for i in range(len(search_list)):
                if self.data[find_idx+i] != search_list[i]:
                    end = False
                    break
                end = True
            if end == False:
                continue
            break
        return find_idx

    def to_ida_binary(self):
        with open('./colbert_ida', 'wb') as f:
            for data in self.data:
                f.write(chr(data&0xff))
                if data&0x100:
                    f.write('\x01')
                else:
                    f.write('\x00')               
        
        
            
with open('colbert.bin', 'rb') as f:
    d = f.read()

form = Formatter(d)
#print form.toHex(0x0006400, 0x10)
form.to_ida_binary()
#find_idx = form.find([0x176,0xff])
#print hex(find_idx)
#form.to9bit_list(t)


