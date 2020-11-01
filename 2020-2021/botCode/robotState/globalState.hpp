#include "robotStateHistory.hpp"
#include <functional>

// There's an argument to be made there that StateUpdaters should return a new
//    RobotState that is incorporated into the current one
// To take it a step further, we could make the actual state_history object
//    private, and only allow users to access a copy of it. Then, we would make
//    the only way to set the current state through a state_updater. For the
//    moment not yet though
typedef std::function<void()> StateUpdater;

class GlobalState {
  private:
    static std::vector<StateUpdater> state_updaters;

  public:
    static RobotStateHistory state_history;
    static double get(SD sd);
    static void set(SD sd, double val);
    static RobotState current_state();
    static RobotState states_ago(int n);
    static void add_state_updater(StateUpdater s);
    static void update_state();
};