#include "testEstimator.hpp"

namespace TestEstimator {
std::default_random_engine generator;
std::normal_distribution<double> distribution(0.0, 0.1);
} // namespace TestEstimator

RobotState estimatorF(RobotStateHistory state_history, bool use_uncertianty) {
    RobotState new_state = RobotState();
    if (use_uncertianty) {
        new_state.set(SD::Angle, state_history.get_past(SD::Angle, 1, 0.0) +
                                     TestEstimator::distribution(
                                         TestEstimator::generator));
    } else {
        new_state.set(SD::Angle, 0.0);
    }
    return new_state;
}

const std::unordered_set<SD> past_sds_using({SD::Angle});
const std::unordered_set<SD> sds_using({});
const std::unordered_set<SD> sds_estimating(past_sds_using);
StateEstimator getTestEstimator() {
    return StateEstimator(estimatorF, past_sds_using, sds_using,
                          sds_estimating);
}