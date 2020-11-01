#include "globalState.hpp"

std::vector<StateUpdater> state_updaters = std::vector<StateUpdater>();
RobotStateHistory GlobalState::state_history = RobotStateHistory();
RobotState GlobalState::current_state() {
    return GlobalState::state_history.current_state();
}
RobotState GlobalState::states_ago(int n) {
    return GlobalState::state_history.states_ago(0);
}
double GlobalState::get(SD sd) { return GlobalState::current_state().get(sd); }
void GlobalState::set(SD sd, double val) {
    GlobalState::current_state().set(sd, val);
};
void GlobalState::add_state_updater(StateUpdater state_updater) {
    state_updaters.push_back(state_updater);
};
void GlobalState::update_state() {
    GlobalState::state_history.add_state(GlobalState::current_state().clone());
    for (int i = 0; i < GlobalState::state_updaters.size(); i++) {
        GlobalState::state_updaters[i]();
    }
}
