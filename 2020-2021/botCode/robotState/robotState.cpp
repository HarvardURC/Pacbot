#include "robotState.hpp"

#include <string>

RobotState::RobotState(std::unordered_map<SD, double, SDHash> data) {
    this->data = data;
}
RobotState::RobotState() {
    RobotState(std::unordered_map<SD, double, SDHash>());
}

std::string SD_to_string(SD sd) {
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
bool RobotState::contains(SD sd) { return this->data.count(sd); }
bool RobotState::get(SD sd) {
    throw_if_not_found("RobotState.get", sd);
    return this->data[sd];
}
void RobotState::set(SD sd, double val) {
    throw_if_not_found("RobotState.set", sd);
    this->data[sd] = val;
}
void RobotState::remove(SD sd) { this->data.erase(sd); }
double RobotState::pop(SD sd) {
    try {
        int val = get(sd);
        remove(sd);
        return val;
    } catch (sd_not_found_exception &e) {
        throw sd_not_found_exception("RobotState.pop", sd);
    }
}

std::unordered_set<SD, SDHash> RobotState::get_keys() {
    std::unordered_set<SD, SDHash> keys = std::unordered_set<SD, SDHash>();
    for (auto entry : this->data) {
        keys.insert(entry.first);
    }
    return keys;
}

RobotState RobotState::clone() {
    return RobotState(std::unordered_map<SD, double, SDHash>(this->data.begin(),
                                                             this->data.end()));
}