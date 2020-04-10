### automatically saves workspaces
winddbg -QY basic_vuln.exe c:\class\crash_file 

K (display stack backtrace information)
p (step over)
t (step into)

### masm evaluation mode
<p>? (evaluation)<br>
e.g  ?esp <br>
     ?esp+100 <br>
     ?esp+ecx+100  <br> 
</p>
### Inspect arbitrary memory 
<p>dd esp <br> 
dd poi(esp)   (poi works like a pointer, extract the value from esp, and go to that value) <br>
</p>

