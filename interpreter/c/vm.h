#ifndef clox_vm_h
#define clox_vm_h

#include "chunk.h"


// ip, instruction pointer, is to keep track of where the VM is.
// dereferencing a pointer is faster then doing an element lookup.
// The ip points to the instruction that is to be executed next
typedef struct {
    Chunk* chunk;
    uint8_t* ip; 
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR
} InterpretResult;

void initVM();
void freeVM();

InterpretResult interpret(Chunk* chunk);

#endif