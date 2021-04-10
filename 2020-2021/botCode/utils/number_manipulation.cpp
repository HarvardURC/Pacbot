#include <chrono>
#include <stdio.h>

int modulo(int a, int b) {
    int remainder = a % b;
    return remainder < 0 ? remainder + b : remainder;
}

unsigned get_rand_seed() {
    return std::chrono::system_clock::now().time_since_epoch().count();
}