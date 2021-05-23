#ifndef ROBOT_STATE_HISTORY_H
#define ROBOT_STATE_HISTORY_H

#include "../dataTypes/deque.cpp"
#include "robotState.hpp"

typedef std::shared_ptr<const RobotState> history_el_t;
typedef Deque<history_el_t> history_t;

class RobotStateHistory {

  private:
    std::unique_ptr<RobotState> current_state;
    std::shared_ptr<history_t> state_history;
    history_el_t states_ago_ptr(int n);

  public:
    static const int DEFAULT_MAX_SIZE = 10;
    RobotStateHistory(int max_size = DEFAULT_MAX_SIZE);
    RobotStateHistory(std::shared_ptr<history_t> state_history);
    RobotStateHistory(const RobotStateHistory &state_history);
    RobotStateHistory &operator=(const RobotStateHistory &state_history);
    int get_max_size();
    int get_size();
    RobotState get_current_state();
    // This doesn't allow you to edit earlier states
    void add_state(RobotState robot_state);
    void add_empty_state();
    RobotState states_ago(int n);
    Deque<std::optional<double>> get_SD_history(SD sd);
    bool contains(SD sd);
    double get(SD sd);
    void set(SD sd, double val);
    double get_past(SD sd, int states_ago, double default_);
    double get_past_unsafe(SD sd, int states_ago);
    double get_past_last_default(SD sd, int states_ago);
    double pop(SD sd);
    void set_max_size(int max_size);
    std::unordered_set<SD, SDHash> get_keys();
    void use_all(RobotState robot_state);
};
#endif