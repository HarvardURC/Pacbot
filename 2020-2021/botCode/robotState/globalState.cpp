#include "globalState.hpp"

RobotState GlobalState::get_current_state() {
    return GlobalState::state_history.get_current_state();
}
RobotState GlobalState::states_ago(int n) {
    return GlobalState::state_history.states_ago(0);
}
double GlobalState::get(SD sd) { return GlobalState::state_history.get(sd); }
void GlobalState::set(SD sd, double val) {
    GlobalState::state_history.set(sd, val);
}
void GlobalState::add_state_updater(StateUpdater state_updater) {
    GlobalState::state_updaters.push_back(state_updater);
}
void GlobalState::add_state_estimator(StateEstimator state_estimator) {
    GlobalState::state_estimators.push_back(state_estimator);
}
void GlobalState::update_state() {
    RobotState new_state = GlobalState::get_current_state();
    for (int i = 0; i < GlobalState::state_updaters.size(); i++) {
        new_state.use(GlobalState::state_updaters[i]());
    }
    GlobalState::state_history.add_state(new_state);
    for (int i = 0; i < GlobalState::state_estimators.size(); i++) {
        RobotState to_use =
            GlobalState::state_estimators[i](GlobalState::state_history);
        GlobalState::state_history.use(to_use);
    }
}
