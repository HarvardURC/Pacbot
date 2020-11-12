#include "masterEstimator.hpp"

void apply_state_estimator(StateEstimator state_estimator,
                           RobotStateHistory robot_state_history) {
    RobotState new_state = state_estimator(robot_state_history);
    robot_state_history.use(new_state);
}