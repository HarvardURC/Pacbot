#include "particleFilter.hpp"
#include "../utils/number_manipulation.hpp"

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
    apply_state_estimator(this->estimator, &state_history, true);
    return state_history;
}

std::vector<double> ParticleFilter::getProbabilities(
    std::vector<RobotStateHistory> state_histories) {
    std::vector<double> probabilities;
    for (RobotStateHistory history : state_histories) {
        probabilities.push_back(this->judge(history));
    }
    double sum = 0;
    for (double prob : probabilities) {
        sum += prob;
    }
    for (int i = 0; i < probabilities.size(); i++) {
        probabilities[i] = probabilities[i] / sum;
    }
    return probabilities;
}

particle ParticleFilter::choose_particle() {
    double rand_num = this->weight_dist(this->weight_geneator);
    int max_probability = 0;
    for (particle particle : this->particles) {
        max_probability += particle.probability;
        if (max_probability >= rand_num) {
            return particle;
        }
    }
    return this->particles[this->particles.size() - 1];
}

void ParticleFilter::addState(RobotState new_state) {
    std::vector<RobotStateHistory> new_states;
    for (int i = 0; i < this->num_particles; i++) {
        new_states.push_back(this->updateState(
            this->choose_particle().state_history, new_state));
    }
    std::vector<double> probabilities = this->getProbabilities(new_states);
    std::vector<particle> new_particles;
    for (int i = 0; i < this->num_particles; i++) {
        particles.push_back(particle(new_states[i], probabilities[i]));
    }
    this->particles = new_particles;
}

RobotStateHistory ParticleFilter::most_likely() {
    particle best_particle = this->particles[0];
    for (particle particle : this->particles) {
        if (particle.probability > best_particle.probability) {
            best_particle = particle;
        }
    }
    return best_particle.state_history;
}

RobotState ParticleFilter::estimate(RobotStateHistory state) {

    this->addState(state.get_current_state());
    return this->most_likely().get_current_state();
}