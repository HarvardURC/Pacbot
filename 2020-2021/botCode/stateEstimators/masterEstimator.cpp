#include "masterEstimator.hpp"

// Estimators are to signify models that use measurments to make inferences
//    about our state

StateEstimator::StateEstimator(StateEstimator::StateEstimatorF f,
                               std::unordered_set<SD> past_sds_using,
                               std::unordered_set<SD> sds_using,
                               std::unordered_set<SD> sds_estimating) {
    this->f = f;
    this->past_sds_using = past_sds_using;
    this->sds_using = sds_using;
    this->generator = std::default_random_engine(get_rand_seed());
    this->sds_estimating = sds_estimating;
}

void StateEstimator::apply(std::shared_ptr<RobotStateHistory> state_history,
                           bool with_uncertianity) {
    // Plasubile that we should enforce sds_using and sds_estimating
    RobotState new_state = this->f(state_history->trimmed_copy(this->sds_using),
                                   with_uncertianity);
    state_history->use_all(new_state);
}
