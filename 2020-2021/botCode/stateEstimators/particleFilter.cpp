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
    this->gen = std::default_random_engine(get_rand_seed());
    this->distribution = std::uniform_real_distribution<double>(0.0, 1.0);
    this->num_particles = num_particles;
    particle startingParticle =
        particle(std::shared_ptr<RobotStateHistory>(
                     new RobotStateHistory(startingState)),
                 1.);
    this->particles.push_back(startingParticle);
}

RobotStateHistory ParticleFilter::updateState(RobotStateHistory state_history,
                                              RobotState new_state) {
    state_history.add_state(new_state);
    this->estimator.apply(&state_history, true);
    return state_history;
}

// Creates a vector of doubles where each probability is proportional to its
// weight and all the probabilties sum to 1
std::vector<double> ParticleFilter::getProbabilities(
    std::vector<std::shared_ptr<RobotStateHistory> /**/> state_histories) {
    std::vector<double> probabilities;
    for (std::shared_ptr<RobotStateHistory> history : state_histories) {
        probabilities.push_back(this->judge(*history));
    }
    double sum =
        std::accumulate(probabilities.begin(), probabilities.end(), 0.0);
    for (int i = 0; i < probabilities.size(); i++) {
        probabilities[i] = probabilities[i] / sum;
    }
    return probabilities;
}

// Samples a random particle, with likelyhood of a particle being chosen
// equal to its probability
particle ParticleFilter::chooseParticle() {
    // Random num between 0.0 and 1.0, as sum of particle probablities should be
    // 1
    double rand_num = this->distribution(this->gen);
    double max_probability = 0;
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
    // Creates a vector if update state histories
    std::vector<std::shared_ptr<RobotStateHistory>> new_states;
    for (int i = 0; i < this->num_particles; i++) {
        // Sasmple a particle, then update and add its state history
        std::shared_ptr<RobotStateHistory> chosen_history =
            this->chooseParticle().state_history;
        RobotStateHistory new_state_history =
            this->updateState(*chosen_history, new_state);
        new_states.push_back(std::shared_ptr<RobotStateHistory>(
            new RobotStateHistory(new_state_history)));
    }

    // Get a vector corresponding to the judgment for each particle
    std::vector<double> probabilities = this->getProbabilities(new_states);
    // Resets new particle vector by effectivelly ziping new_states and
    // probabilities

    this->particles = std::vector<particle>();
    for (int i = 0; i < this->num_particles; i++) {
        this->particles.push_back(particle(new_states[i], probabilities[i]));
    }
}

bool particle_compare(particle p1, particle p2) {
    return p1.probability < p2.probability;
}

/**
Finds and returns the state_history from the single particle with the highest
proability
*/
RobotState ParticleFilter::getState() {
    RobotState state = RobotState();
    for (SD sd : this->sds_estimating) {
        double sum = 0.0;
        for (particle particle : this->particles) {
            sum += particle.state_history->get(sd);
        }
        state.set(sd, sum / this->particles.size());
    }
    return state;
}

RobotState ParticleFilter::estimate(RobotStateHistory &state) {
    this->addState(state.get_current_state());
    return this->getState();
}