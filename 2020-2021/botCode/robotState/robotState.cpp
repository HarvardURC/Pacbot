#include "robotState.hpp"

#include <string>

RobotState::RobotState(std::unordered_map<SD, double, SDHash> data)
    : data(&data) {}
RobotState::RobotState() {
    this->data = std::unique_ptr<std::unordered_map<SD, double, SDHash> /**/>(
        new std::unordered_map<SD, double, SDHash>());
}
RobotState::RobotState(const RobotState &robot_state)
    : data(new data_t(*robot_state.data)) {}
RobotState &RobotState::operator=(const RobotState &robot_state) {
    this->data.reset(new data_t(*robot_state.data));
    return *this;
}
std::string RobotState::sd_to_string(SD sd) {
    std::unordered_map<SD, std::string, SDHash> sd_string_map =
        std::unordered_map<SD, std::string, SDHash>();
    sd_string_map[Row] = "Row";
    sd_string_map[Col] = "Col";
    sd_string_map[Angle] = "Angle";
    sd_string_map[Time] = "Time";
    return sd_string_map[sd];
}

RobotState::sd_not_found_exception::sd_not_found_exception(
    std::string proc_name, SD sd) {
    this->proc_name = proc_name;
    this->sd = sd;
}
void RobotState::throw_if_not_found(std::string proc_name, SD sd) const {
    if (!this->contains(sd)) {
        throw sd_not_found_exception(proc_name, sd);
    }
}

bool RobotState::contains(SD sd) const { return this->data->count(sd) == 1; }
double RobotState::get(SD sd) const {
    throw_if_not_found("RobotState.get", sd);
    return this->data->at(sd);
}
std::optional<double> RobotState::geto(SD sd) const {
    if (this->contains(sd)) {
        return this->get(sd);
    } else {
        return {};
    }
}
void RobotState::set_override(SD sd, double val) { (*this->data)[sd] = val; }
void RobotState::set(SD sd, double val) {
    if (this->contains(sd)) {
        throw std::invalid_argument(
            // clang-format off
            "Attempted to set value for " + sd_to_string(sd) +
            ", but it already has a value. Try set_override if you would like to override the previous value."
            // clang-format on
        );
    } else {
        (*this->data)[sd] = val;
    }
}
void RobotState::remove(SD sd) { this->data->erase(sd); }
double RobotState::pop(SD sd) {
    try {
        int val = get(sd);
        remove(sd);
        return val;
    } catch (sd_not_found_exception &e) {
        throw sd_not_found_exception("RobotState.pop", sd);
    }
}

std::unordered_set<SD, SDHash> RobotState::get_keys() const {
    std::unordered_set<SD, SDHash> keys = std::unordered_set<SD, SDHash>();
    for (auto itr = this->data->begin(); itr != this->data->end(); itr++) {
        keys.insert((*itr).first);
    }
    return keys;
}
void RobotState::cut_down_to(RobotState robot_state,
                             std::unordered_set<SD> to_use) {
    for (SD sd : robot_state.get_keys()) {
        if (to_use.find(sd) == to_use.end()) {
            this->remove(sd);
        }
    }
}
void RobotState::use_all(RobotState robot_state) {
    for (SD sd : robot_state.get_keys()) {
        this->set_override(sd, robot_state.get(sd));
    }
}
void RobotState::use(RobotState robot_state, std::unordered_set<SD> to_use) {
    for (SD sd : robot_state.get_keys()) {
        if (to_use.find(sd) != to_use.end()) {
            this->set_override(sd, robot_state.get(sd));
        }
    }
}
void RobotState::use_extras(RobotState robot_state) {
    auto this_keys = this->get_keys();
    for (SD sd : robot_state.get_keys()) {
        if (this_keys.find(sd) == this_keys.end()) {
            this->set(sd, robot_state.get(sd));
        }
    }
}

std::unordered_map<SD, double, SDHash> RobotState::get_data() const {
    return *this->data;
}

void RobotState::trim_to(std::unordered_set<SD> to_keep) {
    for (SD sd : this->get_keys()) {
        if (to_keep.count(sd) == 0) {
            this->remove(sd);
        }
    }
}