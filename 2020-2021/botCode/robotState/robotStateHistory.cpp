#include "robotStateHistory.hpp"

RobotStateHistory::RobotStateHistory(Deque<RobotState> stateHistory) {
    this->stateHistory = stateHistory.clone();
};
RobotStateHistory::RobotStateHistory(int max_size) {
    this->stateHistory = Deque<RobotState>(max_size);
};