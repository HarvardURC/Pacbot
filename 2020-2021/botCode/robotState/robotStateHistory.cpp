#include "robotStateHistory.hpp"

#include <stdexcept>

RobotStateHistory::RobotStateHistory(Deque<RobotState> stateHistory) {
    this->state_history = stateHistory;
}
RobotStateHistory::RobotStateHistory(int max_size) {
    this->state_history = Deque<RobotState>(max_size);
}
RobotStateHistory::RobotStateHistory(
    const RobotStateHistory &robotStateHistory) {
    this->state_history = robotStateHistory.state_history;
}
int RobotStateHistory::get_max_size() {
    return this->state_history.get_max_size();
}
int RobotStateHistory::get_size() { return this->state_history.length(); }
RobotState RobotStateHistory::states_ago(int n) {
    if (n < 0 || n >= this->get_max_size()) {
        throw std::out_of_range(
            "RobotStateHistory, Index = " + std::to_string(n) +
            ", Length = " + std::to_string(this->get_max_size()));
    } else if (n == 0) {
        return this->current_state;
    } else {
        return this->state_history.get(std::min(n, this->get_max_size()));
    }
}
RobotState RobotStateHistory::get_current_state() {
    return this->states_ago(0);
}
int RobotStateHistory::num_states() { return this->state_history.length(); };
void RobotStateHistory::add_state(RobotState robot_state) {
    this->state_history.add(this->current_state);
    set_current_state(robot_state);
}
void RobotStateHistory::set_current_state(RobotState robot_state) {
    this->current_state = robot_state;
}
RobotState RobotStateHistory::drop_current_state() {
    return this->state_history.pop_first();
}
Deque<double> RobotStateHistory::get_SD_history(SD sd) {
    Deque<double> sd_history = Deque<double>(this->get_max_size());
    for (int i = this->num_states() - 1; i != 0; i--) {
        sd_history.add(states_ago(i).get(sd));
    }
    return sd_history;
}
void RobotStateHistory::set_max_size(int max_size) {
    this->state_history.set_max_size(max_size);
}

bool RobotStateHistory::contains(SD sd) {
    return this->current_state.contains(sd);
}
double RobotStateHistory::get(SD sd) { return this->current_state.get(sd); }
void RobotStateHistory::set(SD sd, double val) {
    return this->current_state.set(sd, val);
}
double RobotStateHistory::pop(SD sd) { return this->current_state.pop(sd); }

void throw_if_out_of_range(int states_ago, int max_size, bool is_max) {
    if (states_ago < 0 || states_ago >= max_size) {
        throw std::out_of_range("Index: " + std::to_string(states_ago) +
                                ", RobotStateHistory " + (is_max ? "max" : "") +
                                " size: " + std::to_string(max_size));
    }
}

double RobotStateHistory::get_past(SD sd, int states_ago, double default_) {
    throw_if_out_of_range(states_ago, this->get_max_size(), true);
    if (states_ago > this->get_size()) {
        return default_;
    } else {
        return this->states_ago(states_ago).get(sd);
    }
}
double RobotStateHistory::get_past_unsafe(SD sd, int states_ago) {
    throw_if_out_of_range(states_ago, this->get_max_size(), true);
    int real_states_ago = std::min(states_ago, this->get_size() - 1);
    return this->states_ago(real_states_ago).get(sd);
}
double RobotStateHistory::get_past_last_default(SD sd, int states_ago) {
    throw_if_out_of_range(states_ago, this->get_size(), false);
    return this->states_ago(states_ago).get(sd);
}
std::unordered_set<SD, SDHash> RobotStateHistory::get_keys() {
    return this->current_state.get_keys();
};
void RobotStateHistory::use(RobotState robot_state) {
    return this->current_state.use(robot_state);
};