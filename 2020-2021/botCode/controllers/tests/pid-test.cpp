#define CATCH_CONFIG_MAIN

#include "../pid.hpp"
#include <catch2/catch.hpp>
#include <chrono>
#include <thread>

bool test_getter() {
    PID pid = PID(0., 0., 0.);
    return pid.get_kp() == 0;
}

bool test_empty() {
    PID pid = PID(1., 1., 1.);
    return pid.get_output() == 0;
}

bool test_p() {
    PID pid = PID(1., 0., 0.);
    pid.add_error(2.);
    pid.add_error(1.);
    return pid.get_output() == 1;
}

bool test_d() {
    PID pid = PID(1., 0., 1.);
    int sleep_time = 500;
    double tolerance = 0.02;
    pid.add_error(1 + sleep_time / 1000.);
    std::this_thread::sleep_for(std::chrono::milliseconds(sleep_time));
    pid.add_error(1);
    return abs(pid.get_output()) < tolerance;
}

bool test_predict() {
    PID pid = PID(1., 0., 3.);
    int sleep_time = 1;
    double tolerance = 0.02;
    pid.add_error(2.);
    std::this_thread::sleep_for(std::chrono::seconds(sleep_time));
    pid.add_error(1.5);
    printf("OUTPUT: %f\n", pid.get_output());
    return abs(pid.get_output()) < tolerance;
}

TEST_CASE("PID Tests") {
    REQUIRE(test_getter());
    REQUIRE(test_p());
    REQUIRE(test_d());
    REQUIRE(test_predict());
}
