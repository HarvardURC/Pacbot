#ifndef MASTER_ESTIMATOR_H
#define MASTER_ESTIMATOR_H

#include "../robotState/robotStateHistory.hpp"

typedef std::function<RobotState(RobotStateHistory)> StateEstimator;

void apply_state_estimator(StateEstimator state_estimator,
                           RobotStateHistory state_history);

#endif