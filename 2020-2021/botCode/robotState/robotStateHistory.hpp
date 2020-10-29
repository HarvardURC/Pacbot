#include "../dataTypes/deque.hpp"
#include "robotState.hpp"

class RobotStateHistory {

  private:
    Deque<RobotState> stateHistory;

  public:
    static const int DEFAULT_MAX_SIZE = 5;
    RobotStateHistory();
    RobotStateHistory(int max_size);
    RobotStateHistory(Deque<RobotState> stateHistory);
    RobotState currentState();
    RobotState statesAgo(int n);
    Deque<RobotState> historyAsDeque();
    int num_states();
    int add_state(RobotState robotState);
    int set_current_state(RobotState robotState);
    int drop_current_state();
    Deque<double> getSDHistory(SD sd);
    RobotStateHistory clone();
};