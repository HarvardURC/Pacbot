#include "testJudge.hpp"

double test_judge(RobotStateHistory stateHistory) {
    return 1 / (0.1 + abs(2 - stateHistory.get(SD::Angle)));
}