#ifndef ROBOT_STATE_HISTORY_H
#define ROBOT_STATE_HISTORY_H

#include "../dataTypes/deque.cpp"
#include "robotState.hpp"

class RobotStateHistory {

  private:
    RobotState current_state;
    Deque<RobotState> state_history;

  public:
    static const int DEFAULT_MAX_SIZE = 10;
    RobotStateHistory(int max_size = DEFAULT_MAX_SIZE);
    RobotStateHistory(Deque<RobotState> state_history);
    RobotStateHistory(const RobotStateHistory &robotStateHistory);
    int get_max_size();
    int get_size();
    RobotState get_current_state();
    // This doesn't allow you to edit earlier states
    RobotState states_ago(int n);
    int num_states();
    void add_state(RobotState robot_state);
    void set_current_state(RobotState robot_state);
    RobotState drop_current_state();
    Deque<double> get_SD_history(SD sd);
    bool contains(SD sd);
    double get(SD sd);
    void set(SD sd, double val);
    double get_past(SD sd, int states_ago, double default_);
    double get_past_unsafe(SD sd, int states_ago);
    double get_past_last_default(SD sd, int states_ago);
    double pop(SD sd);
    void set_max_size(int max_size);
    std::unordered_set<SD, SDHash> get_keys();
    void use(RobotState robot_state);
};
#endif