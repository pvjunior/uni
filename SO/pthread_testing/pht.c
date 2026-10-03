#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

struct argpth{
    int id;
    int* arr;
    int len;
};

int* vet;


void* operar_vet(void* void_args){
    struct argpth* args = (struct argpth*) void_args;
    int* res = malloc(sizeof(int));

    int* arr = args->arr;
    int len = args->len;
    int id = args->id;
    *res = 0;
    double val;

    printf("\n[THREAD %d] initializing op from %d to %d\n", id, arr[0], arr[len]);
    fflush(stdin);
    for(int i = 0; i < len; i++){
        val = arr[i];

        val = sin(val) * cos(val);
        val = pow(fabs(val), 2.5) + sqrt(fabs(val));
        val = log1p(fabs(val)) + exp(-fabs(val));


        *res += (int) val;
    }
    printf("\n[THREAD %d] finalized op from %d to %d. Result: %d\n", id, arr[0], arr[len], *res);
    fflush(stdin);
    return (void*) res;
}

int main(int argc, char* argv[]){
    int size = atoi(argv[1]);
    int n_threads = atoi(argv[2]);

    printf("V: %d and NT: %d\n", size, n_threads);

    vet = (int*) calloc(sizeof(int) * size,sizeof(int));

    for(int i = 0; i < size; i++){
        //vet[i] = i;
    }

    for(int i = 0; i < size; i++){
        //printf("%d ", vet[i]);
    }

    int divs = size / n_threads;
    int rest = (size % n_threads) - 1;

    pthread_t workers[n_threads];
    struct argpth args[n_threads];

    for(int i = 0; i < n_threads; i++){
        
        args[i].id = i;
        args[i].arr = vet + (divs * i);
        args[i].len = divs;
        if (i == n_threads - 1)
            args[i].len += rest;
        
            

        pthread_create(&workers[i], NULL, operar_vet, &args[i]);
    }

    int* rep;
    int res = 0;

    for(int i = 0; i < n_threads; i++){
        pthread_join(workers[i], (void**) &rep);

        res += *rep;
    }

    printf("Final result!!! -> %d\n", res);
}
