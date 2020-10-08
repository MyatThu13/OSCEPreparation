# heap\_theory\_notes

## Malloc Implementation\(Heap Manager\)

 malloc\(\), realloc\(\),free\(\)  
 primary purpose of these funcs - divide up the memory allocated by brk\(\),sbrk\(\) and mmap\(\) system calls into smaller chunks  
 \*\*malloc\(\)\*\* - allocates a chunk of memory  
 \*\*realloc\(\)\*\* - modify size of an existing chunk of memory  
 \*\*free\(\)\*\* - free up memory  
 \*\*calloc\(\)\*\* - initializes data as all zero's \(specify an array of N elements\(number of chunks\),each with a defined size.

## Doug Lea's malloc \(dlmalloc\) implementation

malloc\(\),realloc\(\),free\(\),unlink\(\),free\(\)   


## Chunk Structure

```text

Chunk ->  Prev_Size (4bytes)  

          Size      (4bytes)  

Mem   ->  Data                

```

## Adjacent Chunks in Memory

Prev\_Size Size Data Prev\_Size Size Data   
 &lt;-----Chunk 1-----&gt; &lt;----Chunk 2------&gt;   


**general rule-no two free chunks shoud exist side-by-side in memory withoud being coalesced**   


```text

prev_size 

size -  contains size of the current chunk

        lowest 3 bits used as flags 
 
        lowest bit- **PREV_INUSE(previous chunk is in use) bit** 

        zero - the previous chunk is not in use 

        one - the previous chunk is in use 
 
 Mem - memory address of where data starts within the chunk 

```

## Freed Chunk Structure

```text

 Chunk ->  Prev_Size (4bytes)       

           Size      (4bytes)      

           Forward Pointer (4bytes) 

           Backward Pointer(4bytes) 

 Mem   ->  Old Data                 

```

 When free is called, free\(\) check PREVI\_INUSE bit of the chunk to be freed to see if the current chunk and prior chunkk can be combined  
 fd and bd point into a doubly linked free list. \#\#\# unlink\(\) & frontlink\(\)

```text

unlink() removes chunks from a doubly linked free list
frontlink() inserts new chunks into a doubly linked free list 
unlink() is called by free() when an adjacent chunk is also unused 
```

 \*\*Analogy\*\* - a group of individuals holding hands\(.i.e 10 people are holding hands, creating a linked circle\)  
 After coalescing, \*\*the coalesced chunk may no longer point to the old chunk due to size indexing in the bins.\*\*  
 Because the coalesced chunk's size may be different or greater or smaller than the old chunk's size. \#\#\# Unlink\(\) without checks

```text

;P  current chunk 
;FD forward pointer chunk 
;BK backward pointer chunk 
;fd forward pointer 
;bk backward pointer 

#define unlink(P,BK,FD){ 
  FD = P -> fd;  /* current chunk's forward pointer points to FD chunk.
  BK = P -> bk;  /* current chunk's backward pointer points to BK chunk. 
  /* Now,After unlinking
  FD -> bk = BK; /* FD chunk's backward pointer points to BK chunk. 
  BK -> fd = FD; /* BK chunk's forward pointer points to FD chunk. 
}
```

## Unlink\(\) with checks

```text

;P  current chunk 
;FD forward pointer chunk 
;BK backward pointer chunk 
;fd forward pointer 
;bk backward pointer 

#define unlink(P,BK,FD){ 
  FD = P -> fd;  /* current chunk's forward pointer points to FD chunk.
  BK = P -> bk;  /* current chunk's backward pointer points to BK chunk. 

  if(builtin_expect( FD -> bk != P || BK -> fd != P,0)){
    malloc_print(check_action,"corrupted double-linked list")
  } 
  else {
    FD -> bk = BK; /* FD chunk's backward pointer points to BK chunk. 
    BK -> fd = FD; /* BK chunk's forward pointer points to FD chunk. 
}
```

## Bins,Fasstbins & wilderness chunk

```text

linked list are kept in bins.
total 128 bins,sorted by size 
less than 512 bytes (small bins)
greater than 512 bytes (larger bins)

80 bytes bins (Fastbins)
fastbins - never merged,singly linked , only fd pointer , security issue and can exploit 

Wilderness - ummapped memory area between stack and heap 
             top most chunk(the chunk that can increase the size of the heap) 
```

