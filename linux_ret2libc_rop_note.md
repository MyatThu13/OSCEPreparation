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
buffer  SFP   RET==system() 4-byte_PADD(exit_function_address)  ARG_to_system()

4-byte_PADD will be the return address when system() function finished execution.
</pre>

### Chained Libc Attack 
<pre> 
buffer SFP RET==first_system() RP_of_first_system() first_arg_system  second_system() RP_of_second_system() second_arg_sytem 

#The RP of first and system function must be pop some value from the stack in order to align the esp pointer. 
e.g  POP EBP, retn 
Then, you can chain the sequence as you like. To end the chain, the last RP value can be exit() function. 
</pre>





