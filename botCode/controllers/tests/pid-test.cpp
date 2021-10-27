#include "../pid.hpp"
#include <catch2/catch.hpp>

bool test_1() {
    PID *pid = new PID(0., 0., 0.);
    return pid->get_kp() == 1;
}

TEST_CASE("PID Tests") { REQUIRE(test_1()); }
