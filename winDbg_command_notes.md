### automatically saves workspaces
<pre>winddbg -QY basic_vuln.exe c:\class\crash_file 

K (display stack backtrace information)   
p (step over)
t (step into)
</pre>

### masm evaluation mode
? (evaluation)
e.g  ?esp 
     ?esp+100 
     ?esp+ecx+100  


### Inspect arbitrary memory 
dd esp 
dd poi(esp)   (poi works like a pointer, extract the value from esp, and go to that value) 


### Search the area for the opcode 
s 00400000 l 0040c000 64 A1        ( 64 A1 is opcode of this instruction - mov DWORD ptr from FS:[0] )

### Dump TEB block 
d fs:[0] 

### Perform Exception Analysis 
!analyze -v

### Examine the Exception Chain 
!exchain

### MSEC.dll load and check exploitable or not 
!load winext\msec.dll 
!exploitable 


### byagugan.dll, injectsu.dll & detoured.dll 
!load byakugan 

Byakugan.dll contains 
1.jutsu : set of tools to track buffers in memory, determining what is controlled at crash time, and discover valid return addresses
2.pattern_offset
3.mushishi : framework for anti-debugging detection and defeating anti-debugging techniques
4.tenketsu : vista heap emulator/visualizer

The justsu components contains the following functions 
identBuf / listBuf / rmBuf : find buffers (plain ascii, metasploit patterns, or data from file) in memory…
memDiff                    : compare data in memory with a pattern and mark the changes. 
                             This will help you determining whether e.g. shellcode has been changed/corrupted in memory, 
                             whether certain ‘bad characters’ need to be excluded from shellcode, etc
findReturn                 : search for the addresses that point to a usable function to return to.
searchOpcode               : converts assembler instruction to opcode, AND it lists all executable opcode sequence addresses at the same time.
searchVtptr
trackVal
hunt

### Find the metasploit pattern
!pattern_offset 1000

### List of executable modules 
lm 

### Disassemble at specific address 
u 0x640246f7

