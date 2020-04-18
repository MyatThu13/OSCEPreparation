### Stack Canary Protection 
<pre>
place a 4-byte value onto the stack after the buffer and <b>before the return pointer</b>

Stack Guard - uses a terminator canary to protect <b>return pointer</b>
            - earlier versions of gcc & replaced by SSP(stack smashing protector

Stack Smashing Protect(ProPolice) - default in later versions of gcc
                                  - place a random  canary to protect <b>RP & SFP</b>
                                  - also reoders local variables,protecting them from common attacks.
                                  - urandom doesn't strong? -> reverts back to using a terminator canary. 

<b>Type of canaries</b>
Terminator canary - <b>0x00000aff & 0x000aff0d</b>
                  - 0x00 bad char for strcpy() & 0x0a bad char for gets()
Random canary     - random 4-byte value (/dev/urandom)
Null Canary       - weakest type of canary, containing all 0s.


<b>Notes ***</b> - some stack protectiong protect only RP but do not protect the savaed frame pointer. 
          <b> - overwrite SFP with a valid address on the stack that we control,followed by terminator canary,followed by our shellcode</b>
              - and that can hook flow of execution. 
</pre>
