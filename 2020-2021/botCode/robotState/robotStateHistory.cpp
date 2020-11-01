#include "robotStateHistory.hpp"
#include <stdexcept>

RobotStateHistory::RobotStateHistory(Deque<RobotState> stateHistory) {
    this->state_history = stateHistory.clone();
}
RobotStateHistory::RobotStateHistory(int max_size) {
    this->state_history = Deque<RobotState>(max_size);
}
int RobotStateHistory::get_max_size() {
    return this->state_history.get_max_size();
}
RobotState RobotStateHistory::states_ago(int n) {
    if (n < 0 || n >= this->get_max_size()) {
        throw std::out_of_range(
            "RobotStateHistory, Index = " + std::to_string(n) +
            ", Length = " + std::to_string(this->get_max_size()));
    } else {
        return this->state_history.get(std::min(n, this->get_max_size()));
    }
}
RobotState RobotStateHistory::current_state() { return this->states_ago(0); }
Deque<RobotState> RobotStateHistory::history_as_deque() {
    return this->state_history.clone();
};
int RobotStateHistory::num_states() { return this->state_history.length(); };
void RobotStateHistory::add_state(RobotState robot_state) {
    this->state_history.add(robot_state);
}
void RobotStateHistory::set_current_state(RobotState robot_state) {
    this->state_history.set(0, robot_state);
}
RobotState RobotStateHistory::drop_current_state() {
    return this->state_history.pop();
}
Deque<double> RobotStateHistory::get_SD_history(SD sd) {
    Deque<double> sd_history = Deque<double>(this->get_max_size());
    for (int i = 0; i < this->state_history.length(); i++) {
        sd_history.add_to_end(states_ago(i).get(sd));
    }
    return sd_history;
}
RobotStateHistory RobotStateHistory::clone() {
    return RobotStateHistory(this->state_history);
};