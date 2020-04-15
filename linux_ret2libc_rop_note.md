### Linux Ret2Libc Attack 
<pre> Used when the buffer is too small to hold the shellcode or if the stack is non-executable. 
GNU C Linbrary include printf(),strcpy(),system(),sprintf(), and many others. 
Then we pass an argumentto one of the functions within libc <b>by overwriting the return pointer with the wanted functions address.</b> 



</pre>
