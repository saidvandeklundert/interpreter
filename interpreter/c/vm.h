#ifndef clox_vm_h
#define clox_vm_h

#include "chunk.h"
#include "value.h"

#define STACK_MAX 256

// ip, instruction pointer, is to keep track of where the VM is.
// dereferencing a pointer is faster then doing an element lookup.
// The ip points to the instruction that is to be executed next
//
// to keep track of where in the stack we are, stackTop always points just
// past the last item.
typedef struct {
    Chunk* chunk;
    uint8_t* ip; 
    Value stack[STACK_MAX];
    Value* stackTop; 
} VM;

typedef enum {
    INTERPRET_OK,
    INTERPRET_COMPILE_ERROR,
    INTERPRET_RUNTIME_ERROR
} InterpretResult;

void initVM();
void freeVM();

InterpretResult interpret(const char* source);
void push(Value value);
Value pop();

#endif