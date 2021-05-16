#include "particleFilter.hpp"
#include "../utils/number_manipulation.hpp"
#include <numeric>

ParticleFilter::ParticleFilter(StateEstimator estimator, StateJudge judge,
                               RobotStateHistory startingState,
                               int num_particles)
    : estimator(estimator) {
    this->judge = judge;
    this->sds_estimating = this->estimator.sds_estimating;
    this->sds_using = this->estimator.sds_using;
    this->weight_geneator = std::default_random_engine(get_rand_seed());
    this->weight_dist = std::uniform_real_distribution<double>(0.0, 1.0);
    particle startingParticle = particle(startingState, 1.);
    this->particles.push_back(startingParticle);
}

RobotStateHistory ParticleFilter::updateState(RobotStateHistory state_history,
                                              RobotState new_state) {
    state_history.add_state(new_state);
    this->estimator.apply(&state_history, true);
    return state_history;
}

std::vector<double> ParticleFilter::getProbabilities(
    std::vector<RobotStateHistory> state_histories) {
    std::vector<double> probabilities;
    for (RobotStateHistory history : state_histories) {
        probabilities.push_back(this->judge(&history));
    }
    double sum =
        std::accumulate(probabilities.begin(), probabilities.end(), 0.0);
    for (int i = 0; i < probabilities.size(); i++) {
        probabilities[i] = probabilities[i] / sum;
    }
    return probabilities;
}

particle ParticleFilter::chooseParticle() {
    double rand_num = this->weight_dist(this->weight_geneator);
    int max_probability = 0;
    for (particle particle : this->particles) {
        max_probability += particle.probability;
        if (max_probability >= rand_num) {
            return particle;
        }
    }
    // Safety, in case the random number is exactly 1
    return this->particles[this->particles.size() - 1];
}

void ParticleFilter::addState(RobotState new_state) {
    std::vector<RobotStateHistory> new_states;
    for (int i = 0; i < this->num_particles; i++) {
        new_states.push_back(
            this->updateState(this->chooseParticle().state_history, new_state));
    }
    std::vector<double> probabilities = this->getProbabilities(new_states);
    std::vector<particle> new_particles;
    for (int i = 0; i < this->num_particles; i++) {
        particles.push_back(particle(new_states[i], probabilities[i]));
    }
    this->particles = new_particles;
}

bool particle_compare(particle p1, particle p2) {
    return p1.probability < p2.probability;
}

/**
Finds and returns the state_history from the single particle with the highest
proability
*/
RobotStateHistory ParticleFilter::getStateHistory() {
    particle best_particle = *std::max_element(
        this->particles.begin(), this->particles.end(), particle_compare);
    return best_particle.state_history;
}

RobotState ParticleFilter::estimate(RobotStateHistory state) {

    this->addState(state.get_current_state());
    return this->getStateHistory().get_current_state();
}