#ifndef MASTER_UPDATER_H
#define MASTER_UPDATER_H

#include "masterUpdater.hpp"

void apply_state_updater(StateUpdater state_updater,
                         RobotStateHistory robot_state_history) {
    robot_state_history.use(state_updater());
}

#endif