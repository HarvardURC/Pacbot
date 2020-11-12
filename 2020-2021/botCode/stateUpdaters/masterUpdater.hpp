#include "../robotState/robotStateHistory.hpp"

typedef std::function<RobotState()> StateUpdater;

void apply_state_updater(StateUpdater state_updater,
                         RobotStateHistory robot_state_history);