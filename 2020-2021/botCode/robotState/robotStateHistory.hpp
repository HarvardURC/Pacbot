#ifndef ROBOT_STATE_HISTORY_H
#define ROBOT_STATE_HISTORY_H

#include "../dataTypes/deque.cpp"
#include "robotState.hpp"

typedef std::shared_ptr<const RobotState> history_el_t;
typedef Deque<history_el_t> history_t;

class RobotStateHistory {

  private:
    std::shared_ptr<history_t> state_history;
    history_el_t states_ago_ptr(int n) const;

  public:
    std::unique_ptr<RobotState> current_state;
    static const int DEFAULT_MAX_SIZE = 10;
    RobotStateHistory(int max_size = DEFAULT_MAX_SIZE);
    RobotStateHistory(std::shared_ptr<history_t> state_history);
    RobotStateHistory(const RobotStateHistory &state_history);
    RobotStateHistory &operator=(const RobotStateHistory &state_history);
    int get_max_size() const;
    int get_size() const;
    RobotState get_current_state() const;
    // This doesn't allow you to edit earlier states
    void add_state(const RobotState &robot_state);
    void add_empty_state();
    void set_current_state(const RobotState &robot_state);
    RobotState states_ago(int n) const;
    RobotState states_ago_trimmed(int n, std::unordered_set<SD> to_keep) const;
    Deque<std::optional<double>> get_SD_history(SD sd) const;
    bool contains(SD sd) const;
    double get(SD sd) const;
    void set(SD sd, double val);
    void set_override(SD sd, double val);
    double get_past(SD sd, int states_ago, double default_) const;
    double get_past_unsafe(SD sd, int states_ago) const;
    double get_past_last_default(SD sd, int states_ago) const;
    double pop(SD sd);
    void trim_to(std::unordered_set<SD> to_keep);
    RobotStateHistory trimmed_copy(std::unordered_set<SD> to_keep);
    void set_max_size(int max_size);
    std::unordered_set<SD, SDHash> get_keys() const;
    void use_all(RobotState robot_state);
};
#endif