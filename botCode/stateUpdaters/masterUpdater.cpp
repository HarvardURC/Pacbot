#include "masterUpdater.hpp"

void apply_state_updater(StateUpdater state_updater,
                         RobotStateHistory robot_state_history) {
    robot_state_history.use(state_updater());
}