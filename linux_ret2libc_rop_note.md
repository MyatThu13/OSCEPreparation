### Linux Ret2Libc Attack 
<pre>Used when the buffer is too small to hold the shellcode or if the stack is non-executable. 
GNU C Linbrary include printf(),strcpy(),system(),sprintf(), and many others. 
Then we pass an argumentto one of the functions within libc <b>by overwriting the return pointer with the wanted functions address.</b> 
</pre>

### Some Popular return-to-xxx methods 
<pre><b>ret2strcpy & ret2gets</b>
Potentially overwrite data at any location 

<b>ret2sys</b> 
system() func executes the parameter passed with /bin/sh 

<b>ret2plt</b>
return to PLT,where we obtain a list of functions used within a program. 
overwrite the return pointer with an entry in the PLT and pass the arguments of our choice. 
Used when PIE(position independent executable) is on. It doesn't randomize program image(code segment) and PLT. ?????
</pre>

### Ret2Sys Attack 
<pre>
</pre>
