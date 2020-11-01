#include "../dataTypes/deque.hpp"
#include "robotState.hpp"

class RobotStateHistory {

  private:
    Deque<RobotState> state_history;

  public:
    static const int DEFAULT_MAX_SIZE = 5;
    RobotStateHistory(int max_size = DEFAULT_MAX_SIZE);
    RobotStateHistory(Deque<RobotState> state_history);
    int get_max_size();
    RobotState current_state();
    RobotState states_ago(int n);
    Deque<RobotState> history_as_deque();
    int num_states();
    void add_state(RobotState robot_state);
    void set_current_state(RobotState robot_state);
    RobotState drop_current_state();
    Deque<double> get_SD_history(SD sd);
    RobotStateHistory clone();
};