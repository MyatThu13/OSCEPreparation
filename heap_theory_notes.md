### Malloc Implementation(Heap Manager)
<p> malloc(), realloc(),free() <br>
primary purpose of these funcs - divide up the memory allocated by brk(),sbrk() and mmap() system calls into smaller chunks <br>
 
**malloc()** - allocates a chunk of memory <br>
**realloc()** - modify size of an existing chunk of memory <br>
**free()** - free up memory <br>
**calloc()** - initializes data as all zero's (specify an array of N elements(number of chunks),each with a defined size. 
</p>

### Doug Lea's malloc (dlmalloc) implementation 
<p> malloc(),realloc(),free(),unlink(),free() <br>
 
### Chunk Structure  
<p>Chunk ->  Prev_Size (4bytes)  <br>
             Size      (4bytes)  <br>
   Mem   ->  Data                <br>
</p>

### Adjacent Chunks in Memory 
<p>
Prev_Size Size Data Prev_Size Size Data <br>
<-----Chunk 1-----> <----Chunk 2------> <br>
 </p>
**general rule-no two free chunks shoud exist side-by-side in memory withoud being coalesced** <br>
<p>prev_size <br>
size - **contains size of the current chunk** <br>
        lowest 3 bits used as flags <br>
        lowest bit- **PREV_INUSE(previous chunk is in use) bit** <br>
        zero - the previous chunk is not in use <br>
        one - the previous chunk is in use <br>
        
Mem - **memory address of where data starts within the chunk**  <br>
</p>








