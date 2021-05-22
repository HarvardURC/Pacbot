#ifndef DEQUE_TEST_C
#define DEQUE_TEST_C

#include "../../dataTypes/deque.cpp"
#include <catch2/catch.hpp>
#include <chrono>
#include <thread>

namespace Deque_test {
bool size() {
    Deque<int> deq = Deque<int>(4);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    return deq.size() == 3;
}
bool length_at_max() {
    Deque<int> deq = Deque<int>(4);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    deq.add(3);
    deq.add(4);
    deq.add(5);
    return deq.size() == 4;
}
bool get0() {
    Deque<int> deq = Deque<int>(4);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    return deq.get(0) == 2;
}
bool get1() {
    Deque<int> deq = Deque<int>(4);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    return deq.get(1) == 1;
}
bool test_last() {
    Deque<int> deq = Deque<int>(4);
    deq.add(0);
    deq.add(1);
    deq.add(2);
    printf("LAST: %d\n", deq.last());
    return deq.last() == 0;
}
} // namespace Deque_test

TEST_CASE("Deque Tests") {
    REQUIRE(Deque_test::size());
    REQUIRE(Deque_test::length_at_max());
    REQUIRE(Deque_test::get0());
    REQUIRE(Deque_test::get1());
    REQUIRE(Deque_test::test_last());
}

#endif