#include "stdio.h"
#include "common.h"
#include "chunk.h"
#include "debug.h"
#include "vm.h"



int main(int argc, const char* argv[]) {
    printf("it is starting!\n\n");
    
    initVM();
    Chunk chunk;
    initChunk(&chunk);
    int constant = addConstant(&chunk, 1.2);
    writeChunk(&chunk, OP_CONSTANT, 123);
    writeChunk(&chunk, constant,123);
    writeChunk(&chunk, OP_NEGATE,123);
    writeChunk(&chunk, OP_RETURN,123);

    disassembleChunk(&chunk, "test chunk");
    interpret(&chunk);
    freeVM();
    freeChunk(&chunk);
    printf("main comes to an end!\n\n");
    return 0;
}