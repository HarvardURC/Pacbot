#ifndef ROBOTSTATEHISTORY_TEST_C
#define ROBOTSTATEHISTORY_TEST_C

#include "../../robotState/robotStateHistory.hpp"
#include <catch2/catch.hpp>
#include <chrono>
#include <thread>

namespace RobotStateHistory_test {
bool test_copy() {
    RobotStateHistory state_history = RobotStateHistory();
    SD sd = SD::Angle;
    double og_val = 0.0;
    double new_val = 1.0;
    state_history.set(sd, og_val);
    RobotStateHistory copy = state_history;
    bool copy_starts_correct = copy.get(sd) == og_val;
    copy.set_override(sd, new_val);
    bool copied_correctly = state_history.get(sd) == og_val;
    return copy_starts_correct && copied_correctly;
}
bool size() {
    RobotStateHistory state_history = RobotStateHistory();
    RobotState state;
    state_history.set_current_state(state);
    state_history.add_state(state);
    state_history.add_state(state);
    return state_history.get_size() == 3;
}
bool set_and_get() {
    RobotStateHistory state_history = RobotStateHistory();
    double val = -12112.325;
    SD sd = SD::Angle;
    state_history.set(sd, val);
    return state_history.get(sd) == val;
}
bool add_state_simple() {
    RobotStateHistory state_history = RobotStateHistory();
    RobotState state;
    double val = -12112.325;
    SD sd = SD::Angle;
    state.set(sd, val);
    state_history.add_state(state);
    return state_history.get(sd) == val;
}
bool add_state_seperation() {
    RobotStateHistory state_history = RobotStateHistory();
    RobotState state;
    double val = -12112.325;
    SD sd = SD::Angle;
    state.set(sd, val);
    state_history.add_state(state);
    double val2 = 0.0;
    state.set_override(sd, val2);
    return state_history.get(sd) == val;
}
} // namespace RobotStateHistory_test

TEST_CASE("RobotStateHistory Tests") {
    REQUIRE(RobotStateHistory_test::test_copy());
    REQUIRE(RobotStateHistory_test::size());
    REQUIRE(RobotStateHistory_test::set_and_get());
    REQUIRE(RobotStateHistory_test::add_state_simple());
    REQUIRE(RobotStateHistory_test::add_state_seperation());
}

#endif