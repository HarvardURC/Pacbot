#ifndef GLOBAL_STATE_H
#define GLOBAL_STATE_H

//#include "../stateEstimators/masterEstimator.hpp"
//#include "../stateUpdaters/masterUpdater.hpp"
#include "robotStateHistory.hpp"
#include <functional>

namespace GlobalState {
/*
static std::vector<StateUpdater> state_updaters = std::vector<StateUpdater>();
static std::vector<StateEstimator> state_estimators =
std::vector<StateEstimator>();
*/
static RobotStateHistory state_history;
double get(SD sd);
void set(SD sd, double val);
RobotState get_current_state();
RobotState states_ago(int n);
/*
void add_state_updater(StateUpdater s);
void add_state_estimator(StateEstimator s);
*/
void update_state();
}; // namespace GlobalState

#endif