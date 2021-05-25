#ifndef STATE_JUDGE_H
#define STATE_JUDGE_H

#include "../robotState/robotStateHistory.hpp"

typedef std::function<double(RobotStateHistory)> StateJudge;

#endif