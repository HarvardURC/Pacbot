#ifndef PARTICLE_FILTER_H
#define PARTICLE_FILTER_H

#include "../stateJudges/stateJudge.hpp"
#include "masterEstimator.hpp"
#include <random>

const int DEFAULT_NUM_PARTICLES = 500;

struct particle {
    RobotStateHistory state_history;
    double probability;
    particle(RobotStateHistory state_history, double probability) {
        this->state_history = state_history;
        this->probability = probability;
    }
};
class ParticleFilter {
  private:
    StateJudge judge;
    StateEstimator estimator;
    int num_particles;
    std::vector<particle> particles;

    std::default_random_engine weight_geneator;
    std::uniform_real_distribution<double> weight_dist;
    RobotStateHistory updateState(RobotStateHistory state_history,
                                  RobotState new_state);
    std::vector<double>
    getProbabilities(std::vector<RobotStateHistory> state_histories);
    particle chooseParticle();

  public:
    std::unordered_set<SD> sds_estimating;
    std::unordered_set<SD> sds_using;
    ParticleFilter(StateEstimator estimator, StateJudge judge,
                   RobotStateHistory startingState,
                   int num_particles = DEFAULT_NUM_PARTICLES);
    void addState(RobotState new_state);
    /**
     Finds and returns the state_history from the single particle with the
     highest proability
     */
    RobotStateHistory getStateHistory();
    RobotState estimate(RobotStateHistory state_history);
};

#endif