#ifndef ROBOTSTATE_TEST_C
#define ROBOTSTATE_TEST_C

#include "../../robotState/robotState.hpp"
#include <catch2/catch.hpp>
#include <chrono>
#include <thread>

namespace RobotState_test {
bool simple_get() {
    RobotState state = RobotState();
    double val = 100.5;
    SD sd = SD::Angle;
    state.set(sd, val);
    return state.get(sd) == val;
}
bool override_get() {
    RobotState state = RobotState();
    double val0 = 100;
    double val = 100.5;
    SD sd = SD::X;
    state.set(sd, val0);
    state.set(sd, val);
    return state.get(sd) == val;
}
bool copy() {
    RobotState state = RobotState();
    SD sd = SD::X;
    double val = -100.5;
    state.set(sd, val);
    RobotState copy = state;
    copy.set(sd, 0.0);
    return state.get(sd) == val;
}
bool get_keys() {
    RobotState state = RobotState();
    std::vector<SD> sds;
    sds.push_back(SD::X);
    sds.push_back(SD::Y);
    sds.push_back(SD::Angle);
    for (SD sd : sds) {
        state.set(sd, 0.0);
    }
    auto keys = state.get_keys();
    bool all_matched = true;
    for (SD sd : sds) {
        all_matched = all_matched && (keys.find(sd) != keys.end());
    }
    return all_matched && keys.size() == sds.size();
}
bool contains() {
    RobotState state = RobotState();
    std::vector<SD> sds;
    sds.push_back(SD::X);
    sds.push_back(SD::Y);
    sds.push_back(SD::Angle);
    for (SD sd : sds) {
        state.set(sd, 0.0);
    }
    bool all_matched = true;
    for (SD sd : sds) {
        all_matched = all_matched && state.contains(sd);
    }
    return all_matched;
}
bool use_all() {
    RobotState state1 = RobotState();
    RobotState state2 = RobotState();
    std::vector<SD> sds_shared;
    sds_shared.push_back(SD::X);
    sds_shared.push_back(SD::Y);
    std::vector<SD> sds_extra;
    sds_extra.push_back(SD::Angle);
    double val1 = 0.0;
    double val2 = -1.0;
    for (SD sd : sds_shared) {
        state1.set(sd, val1);
        state2.set(sd, val2);
    }
    for (SD sd : sds_extra) {
        state1.set(sd, val1);
    }
    state1.use_all(state2);
    bool extra_1s_matched = true;
    bool all_2s_matched = true;
    for (SD sd : sds_extra) {
        extra_1s_matched = extra_1s_matched && state1.get(sd) == val1;
    }
    for (SD sd : sds_shared) {
        all_2s_matched = all_2s_matched && state1.get(sd) == val2;
    }
    printf("1s, 2s: %d, %d, %f", extra_1s_matched, all_2s_matched,
           state1.get(SD::Angle));
    return extra_1s_matched && all_2s_matched;
}
} // namespace RobotState_test

TEST_CASE("RobotState Tests") {
    REQUIRE(RobotState_test::contains());
    REQUIRE(RobotState_test::simple_get());
    REQUIRE(RobotState_test::override_get());
    REQUIRE(RobotState_test::copy());
    REQUIRE(RobotState_test::get_keys());
    REQUIRE(RobotState_test::use_all());
}

#endif