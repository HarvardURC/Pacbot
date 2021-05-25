#include "robotStateHistory.hpp"

#include <stdexcept>

int states_ago_to_index(int states_ago) { return states_ago - 1; }

// CONSTRUCTORS
RobotStateHistory::RobotStateHistory(std::shared_ptr<history_t> stateHistory) {
    this->state_history = stateHistory;
    this->current_state = std::unique_ptr<RobotState /**/>(new RobotState());
}
RobotStateHistory::RobotStateHistory(int max_size) {
    this->state_history = std::shared_ptr<history_t>(
        new Deque<history_el_t /**/>(states_ago_to_index(max_size)));
    this->current_state = std::unique_ptr<RobotState /**/>(new RobotState());
}
RobotStateHistory::RobotStateHistory(const RobotStateHistory &state_history)
    : current_state(new RobotState(*state_history.current_state)) {
    this->state_history = state_history.state_history;
}
RobotStateHistory &
RobotStateHistory::operator=(const RobotStateHistory &state_history) {
    this->current_state.reset(new RobotState(*state_history.current_state));
    return *this;
}

// Simple State_history Accessors
int RobotStateHistory::get_max_size() const {
    return this->state_history->get_max_size();
}
// The plus 1 is due to the current_state variable
int RobotStateHistory::get_size() const {
    return this->state_history->size() + 1;
}

void throw_if_out_of_range(int states_ago, int max_size, bool is_max) {
    if (states_ago < 0 || states_ago >= max_size) {
        throw std::out_of_range("Index: " + std::to_string(states_ago) +
                                ", RobotStateHistory " + (is_max ? "max" : "") +
                                " size: " + std::to_string(max_size));
    }
}

// Gets the pointer to n states ago
history_el_t RobotStateHistory::states_ago_ptr(int n) const {
    throw_if_out_of_range(n, this->get_size(), false);
    if (n == 0) {
        throw std::out_of_range("RobotStateHistory, internal error, "
                                "states_ago_ptr called with index 0");
    } else {
        return this->state_history->get(states_ago_to_index(n));
    }
}

// Simple Current_state Accessors
std::unordered_set<SD, SDHash> RobotStateHistory::get_keys() const {
    return this->current_state->get_keys();
};
void RobotStateHistory::use_all(RobotState robot_state) {
    return this->current_state->use_all(robot_state);
};
bool RobotStateHistory::contains(SD sd) const {
    return this->current_state->contains(sd);
}
double RobotStateHistory::get(SD sd) const {
    return this->current_state->get(sd);
}
void RobotStateHistory::set(SD sd, double val) {
    return this->current_state->set(sd, val);
}
void RobotStateHistory::set_override(SD sd, double val) {
    return this->current_state->set_override(sd, val);
}
double RobotStateHistory::pop(SD sd) { return this->current_state->pop(sd); }

// Returns a copy of the robot state n states ago
// Exposed publicly
RobotState RobotStateHistory::states_ago(int n) const {
    if (n == 0) {
        return *this->current_state;
    } else {
        return *this->states_ago_ptr(n);
    }
}
RobotState RobotStateHistory::get_current_state() const {
    return this->states_ago(0);
}

// Adds the current state to the history deque, and then adds given states to
// current_state
void RobotStateHistory::add_state(const RobotState &robot_state) {
    history_el_t el_to_add = history_el_t(new RobotState(*this->current_state));
    this->state_history->add(el_to_add);
    this->current_state =
        std::unique_ptr<RobotState>(new RobotState(robot_state));
}
void RobotStateHistory::add_empty_state() { this->add_state(RobotState()); }
void RobotStateHistory::set_current_state(const RobotState &robot_state) {
    this->current_state =
        std::unique_ptr<RobotState>(new RobotState(robot_state));
}

// Gets a deque with values for just one sd
Deque<std::optional<double>> RobotStateHistory::get_SD_history(SD sd) const {
    Deque<std::optional<double>> sd_history =
        Deque<std::optional<double>>(this->get_max_size());
    for (int i = this->get_size() - 1; i != 0; i--) {
        sd_history.add(this->states_ago_ptr(i)->geto(sd));
    }
    sd_history.add(this->current_state->geto(sd));
    return sd_history;
}
void RobotStateHistory::set_max_size(int max_size) {
    this->state_history->set_max_size(states_ago_to_index(max_size));
}

double RobotStateHistory::get_past(SD sd, int states_ago,
                                   double default_) const {
    throw_if_out_of_range(states_ago, this->get_max_size(), true);
    if (states_ago == 0) {
        return this->get(sd);
    } else if (states_ago > this->get_size()) {
        return default_;
    } else {
        return this->states_ago_ptr(states_ago)->get(sd);
    }
}
double RobotStateHistory::get_past_unsafe(SD sd, int states_ago) const {
    throw_if_out_of_range(states_ago, this->get_max_size(), true);
    if (states_ago == 0) {
        return this->get(sd);
    }
    int real_states_ago = std::min(states_ago, this->get_size() - 1);
    return this->states_ago_ptr(real_states_ago)->get(sd);
}
double RobotStateHistory::get_past_last_default(SD sd, int states_ago) const {
    throw_if_out_of_range(states_ago, this->get_size(), false);
    if (states_ago == 0) {
        return this->get(sd);
    }
    return this->states_ago_ptr(states_ago)->get(sd);
}

void RobotStateHistory::trim_to(std::unordered_set<SD> to_keep) {
    this->current_state->trim_to(to_keep);
}