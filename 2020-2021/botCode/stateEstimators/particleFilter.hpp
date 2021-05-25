#ifndef PARTICLE_FILTER_H
#define PARTICLE_FILTER_H

#include "../stateJudges/stateJudge.hpp"
#include "masterEstimator.hpp"
#include <random>
#include <unordered_set>

const int DEFAULT_NUM_PARTICLES = 500;

struct particle {
    std::shared_ptr<RobotStateHistory> state_history;
    double probability;
    particle(std::shared_ptr<RobotStateHistory> state_history,
             double probability)
        : state_history(state_history) {
        this->probability = probability;
    }
};
class ParticleFilter {
  private:
    StateJudge judge;
    StateEstimator estimator;
    int num_particles;
    std::vector<particle> particles;

    std::default_random_engine gen;
    std::uniform_real_distribution<double> distribution;
    RobotStateHistory updateState(RobotStateHistory state_history,
                                  RobotState new_state);
    std::vector<double> getProbabilities(
        std::vector<std::shared_ptr<RobotStateHistory>> state_histories);
    particle chooseParticle();

  public:
    std::unordered_set<SD> sds_estimating;
    std::unordered_set<SD> past_sds_using;
    std::unordered_set<SD> sds_using;
    ParticleFilter(StateEstimator estimator, StateJudge judge,
                   RobotStateHistory startingState,
                   int num_particles = DEFAULT_NUM_PARTICLES);
    void addState(RobotState new_state,
                  RobotState previous_state = RobotState());
    /**
     @return state_history from the single particle with the highest proability
     */
    RobotState getState();
    RobotState estimate(RobotStateHistory &state_history);
};

#endif