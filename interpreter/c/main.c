#include "common.h"
#include "chunk.h"
#include "stdio.h"

int main(int argc, const char* argv[]) {
    printf("it is starting!");
    Chunk chunk;
    initChunk(&chunk);
    writeChunk(&chunk, OP_RETURN);
    freeChunk(&chunk);
    printf("main comes to an end!");
    return 0;
}