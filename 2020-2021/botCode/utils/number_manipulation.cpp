#include <stdio.h>

int modulo(int a, int b) {
    int remainder = a % b;
    return remainder < 0 ? remainder + b : remainder;
}