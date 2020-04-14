## Linux Shellcoding 
<pre>
System Calls 
eax - desired sys call number 
ebx,ecx,edx,..... - arguments

Full list of sys calls - <b>/usr/include/asm-i386/unistd.h</b>

On Linux 32 & 64 , sys call are static.

Spawning a root shell - Many binarys drop privileges (even SUID bits on)
So, need to restore rights, 
<b>setreuid() sys call is needed.</b> 
</pre>

### Removing Null bytes 
<pre> 
<b>1.Use aprropriate 32bits, 16 bits or 8 bits register size for the value </b>
e.g 
    mov eax,0xa -> this cause null bytes. 
So use this,   mov al,0xa  (caouse 0xa is only 8 bits and this remove null bytes)

<b>2. For moving the zero value into a register </b>
 e.g
     xor eax,eax 
     sub eax,eax 
     mov eax,ecx (Of course,ecx must contains zero value.)
     
You can also use (inc) & (dec) instructions.
</pre>






     
     
