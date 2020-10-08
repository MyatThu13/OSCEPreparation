# winDbg\_command\_notes

## automatically saves workspaces

```text
winddbg -QY basic_vuln.exe c:\class\crash_file 

K (display stack backtrace information)   
p (step over)
t (step into)
```

## masm evaluation mode

```text
? (evaluation)
e.g  ?esp 
     ?esp+100 
     ?esp+ecx+100  
```

## Inspect arbitrary memory

```text
dd esp 
dd poi(esp)   (poi works like a pointer, extract the value from esp, and go to that value) 
```

## Search the area for the opcode

```text
s 00400000 l 0040c000 64 A1        ( 64 A1 is opcode of this instruction - mov DWORD ptr from FS:[0] )
```

## Dump TEB block

```text
d fs:[0] 
```

## Perform Exception Analysis

```text
!analyze -v
```

## Examine the Exception Chain

```text
!exchain
```

## MSEC.dll load and check exploitable or not

```text
!load winext\msec.dll 
!exploitable 
```

## byagugan.dll, injectsu.dll & detoured.dll

```text
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
```

## Find the metasploit pattern

```text
!pattern_offset 1000
```

## Disassemble at specific address

```text
u 0x640246f7
```

## Switch WinDbg between 32 bits and 64 bit modes

```text
!wow64exts.sw 
```

## Symobls

```text
Add a default symbol file path
SRV*C:\windbgsymbols*http://msdl.microsoft.com/download/symbols

Append a symbol search path to the default one before debugging
.sympath+C:\symbol_path 
After appending a symbol path, then reload
.reload 

Checking Symbols
See what modules have symbols loaded 
x *!

Search for all symbols in kernel32 whose name starts with virtual 
x kernel32!virtual* 

Another example 
x *!messagebox* 

load sybmbols for all modules 
ld*
```

## Remote Debugging

```text
To debug a program remotely,2 options available
First, if your are already debugging  a program locally on machine A,tye this command 
to start debugging server within winDbg 
.server tcp:port=1234 

Then,on machine B, File -> Connect to Remote Session and enter this command to connect windDbg Server on machine A
tcp:Port=1234,Server=(IP of Machine A) 

Second Method, On machine A,run dbgsrv to strat a debugging server
dbgsrv.exe -t tcp:port=1234 

On Machine B, File -> Connect to Remote Stub and enter this command
tcp:Port=1234,Server=(IP of Machine A)
```

## Modules

```text
List all loaded modules
lmf 

List a specific module
lmf m ntdll 

Get Image header information of a module
lmf m ntdll 
!dh ntdll (or) !dh start_address_of_module(77790000) 
Notes : ! means that this command is an extercommand which is exported from an external DLL and 
           called inside WinDbg
```

