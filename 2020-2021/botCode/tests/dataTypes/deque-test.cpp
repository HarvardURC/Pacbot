#ifndef DEQUE_TEST_C
#define DEQUE_TEST_C

#include "../../dataTypes/deque.cpp"
#include <catch2/catch.hpp>
#include <chrono>
#include <thread>

namespace Deque_test {
bool length() {
    Deque<int> deq = Deque<int>(4);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    return deq.length() == 3;
}
bool test_last() {
    Deque<int> deq = Deque<int>(3);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    return deq.last() == 1;
}
} // namespace Deque_test

TEST_CASE("Deque Tests") {
    REQUIRE(Deque_test::length());
    REQUIRE(Deque_test::test_last());
}

#endif