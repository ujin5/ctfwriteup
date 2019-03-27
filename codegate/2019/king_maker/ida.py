def PatchArr(dest, length, key1):
 for i in range(0,length,4):
  for j, c in enumerate(key1):
   idc.PatchByte(dest+i+j, Byte(dest+i+j)^ord(c))
# usage: patchArr(start address, string of bytes to write)
#PatchArr(0x4033FF, 0x1e,"lOv3")
#PatchArr(0x4033FF, 0x1e,"lOv3")
#PatchArr(0x4033FF, 0x1e,"lOv3")

