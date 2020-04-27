### automatically saves workspaces
<pre>winddbg -QY basic_vuln.exe c:\class\crash_file 

K (display stack backtrace information)   
p (step over)
t (step into)
</pre>

### masm evaluation mode
<pre>? (evaluation)
e.g  ?esp 
     ?esp+100 
     ?esp+ecx+100  
</pre>

### Inspect arbitrary memory 
<pre>dd esp 
dd poi(esp)   (poi works like a pointer, extract the value from esp, and go to that value) 
</pre>

### Search the area for the opcode 
<pre>s 00400000 l 0040c000 64 A1        ( 64 A1 is opcode of this instruction - mov DWORD ptr from FS:[0] )
</pre>

### Dump TEB block 
<pre>d fs:[0] 
</pre>

### Perform Exception Analysis 
<pre>!analyze -v
</pre>

### Examine the Exception Chain 
<pre>!exchain
</pre>


### MSEC.dll load and check exploitable or not 
<pre>!load winext\msec.dll 
!exploitable 
</pre>

### byagugan.dll, injectsu.dll & detoured.dll 
<pre>!load byakugan 

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
</pre>

### Find the metasploit pattern
<pre>!pattern_offset 1000
</pre>

### List of executable modules 
<pre>lm 
</pre>

### Disassemble at specific address 
<pre>u 0x640246f7
</pre>

### Switch WinDbg between 32 bits and 64 bit modes 
<pre>!wow64exts.sw 
</pre> 

### Symobls 
<pre><b>Add a default symbol file path</b>
SRV*C:\windbgsymbols*http://msdl.microsoft.com/download/symbols

<b>Append a symbol search path to the default one before debugging</b>
.sympath+C:\symbol_path 
<b>After appending a symbol path, then reload</b>
.reload 

<b>Checking Symbols
See what modules have symbols loaded</b> 
x *!

<b>Search for all symbols in kernel32 whose name starts with virtual</b> 
x kernel32!virtual* 

Another example 
x *!messagebox* 

<b>load sybmbols for all modules</b> 
ld*
</pre> 

### Remote Debugging
<pre><b>To debug a program remotely,2 options available
First, if your are already debugging  a program locally on machine A,tye this command 
to start debugging server within winDbg</b> 
.server tcp:port=1234 

<b>Then,on machine B, File -> Connect to Remote Session and enter this command to connect windDbg Server on machine A</b>
tcp:Port=1234,Server=(IP of Machine A) 

<b>Second Method, On machine A,run dbgsrv to strat a debugging server</b>
dbgsrv.exe -t tcp:port=1234 

<b>On Machine B, File -> Connect to Remote Stub and enter this command</b>
tcp:Port=1234,Server=(IP of Machine A)








