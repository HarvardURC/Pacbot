#include "wheelPos.hpp"

RobotState wheelPosEstimatorF(RobotStateHistory state_history,
                              bool use_uncertianty) {
    RobotState new_state = RobotState();
    new_state.set(SD::LW_pos, state_history.get_past(SD::LW_pos, 1, 0.) +
                                  state_history.get(SD::LW_change));
    new_state.set(SD::RW_pos, state_history.get_past(SD::RW_pos, 1, 0.) +
                                  state_history.get(SD::RW_change));
    return new_state;
}

const std::unordered_set<SD> past_sds_using({SD::LW_pos, SD::RW_pos});
const std::unordered_set<SD> sds_using({SD::LW_change, SD::RW_change});
const std::unordered_set<SD> sds_estimating(past_sds_using);
StateEstimator getWheelPosEstimator() {
    return StateEstimator(wheelPosEstimatorF, past_sds_using, sds_using,
                          sds_estimating);
}