This code will create an array of integers and perform several CPU-heavy math operations with each element.
Operations on the array can be divided semi-equally by adding more threads, which will... uh... make the program end sooner... duuh.

### Syntax:
```
gcc pht.c -lm && time ./a.out <array size> <number of threads>
```

### Example with 1215752192 integers on 1 thread:
```
gcc pht.c -lm && time ./a.out 1215752192 1
```

### Example with 1215752192 integers on 4 threads:
```
gcc pht.c -lm && time ./a.out 1215752192 4
```
\
it caps above 1215752192 \
this code can surely explode your computer (not due processing, but due bad coding), so don't push it.