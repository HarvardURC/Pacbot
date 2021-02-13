#ifndef MASTER_UPDATER_H
#define MASTER_UPDATER_H

#include "../robotState/robotStateHistory.hpp"

typedef std::function<RobotState()> StateUpdater;

void apply_state_updater(StateUpdater state_updater,
                         RobotStateHistory robot_state_history);

#endif