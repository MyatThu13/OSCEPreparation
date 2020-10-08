# Stack Canary Protection

```text

place a 4-byte value onto the stack after the buffer and before the return pointer

Stack Guard - uses a terminator canary to protect return pointer
            - earlier versions of gcc & replaced by SSP(stack smashing protector

Stack Smashing Protect(ProPolice) - default in later versions of gcc
                                  - place a random  canary to protect RP & SFP
                                  - also reoders local variables,protecting them from common attacks.
                                  - urandom doesn't strong? -> reverts back to using a terminator canary. 

Type of canaries
Terminator canary - 0x00000aff & 0x000aff0d
                  - 0x00 bad char for strcpy() & 0x0a bad char for gets()
Random canary     - random 4-byte value (/dev/urandom)
Null Canary       - weakest type of canary, containing all 0s.


Notes *** - some stack protectiong protect only RP but do not protect the savaed frame pointer. 
          - overwrite SFP with a valid address on the stack that we control,followed by terminator canary,followed by our shellcode
          - and that can hook flow of execution. 
```

