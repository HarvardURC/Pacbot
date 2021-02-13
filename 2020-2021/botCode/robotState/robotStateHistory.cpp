#include "robotStateHistory.hpp"

#include <stdexcept>

RobotStateHistory::RobotStateHistory(std::deque<RobotState> stateHistory) {
    this->state_history = stateHistory;
}
RobotStateHistory::RobotStateHistory(int max_size) {
    this->state_history = std::deque<RobotState>(0);
    this->set_max_size(max_size);
}
int RobotStateHistory::get_max_size() { return this->state_history.max_size(); }
RobotState RobotStateHistory::states_ago(int n) {
    if (n < 0 || n >= this->get_max_size()) {
        throw std::out_of_range(
            "RobotStateHistory, Index = " + std::to_string(n) +
            ", Length = " + std::to_string(this->get_max_size()));
    } else if (n == 0) {
        return this->current_state;
    } else {
        return this->state_history[std::min(n, this->get_max_size())];
    }
}
RobotState RobotStateHistory::get_current_state() {
    return this->states_ago(0);
}
int RobotStateHistory::num_states() { return this->state_history.size(); };
void RobotStateHistory::add_state(RobotState robot_state) {
    this->state_history.push_front(this->current_state);
    set_current_state(robot_state);
}
void RobotStateHistory::set_current_state(RobotState robot_state) {
    this->current_state = robot_state;
}
void RobotStateHistory::drop_current_state() {
    return this->state_history.pop_front();
}
std::deque<double> RobotStateHistory::get_SD_history(SD sd) {
    std::deque<double> sd_history = std::deque<double>(this->get_max_size());
    for (int i = 0; i < this->num_states(); i++) {
        sd_history.push_back(states_ago(i).get(sd));
    }
    return sd_history;
}
void RobotStateHistory::set_max_size(int max_size) {
    this->state_history.resize(max_size);
}

bool RobotStateHistory::contains(SD sd) {
    return this->current_state.contains(sd);
}
bool RobotStateHistory::get(SD sd) { return this->current_state.get(sd); }
void RobotStateHistory::set(SD sd, double val) {
    return this->current_state.set(sd, val);
}
double RobotStateHistory::pop(SD sd) { return this->current_state.pop(sd); }
std::unordered_set<SD, SDHash> RobotStateHistory::get_keys() {
    return this->current_state.get_keys();
};
void RobotStateHistory::use(RobotState robot_state) {
    return this->current_state.use(robot_state);
};