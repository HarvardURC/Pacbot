#include "particleFilter.hpp"
#include "../utils/data_type_helpers.hpp"
#include "../utils/number_manipulation.hpp"

#include <numeric>

ParticleFilter::ParticleFilter(StateEstimator estimator, StateJudge judge,
                               RobotStateHistory starting_state,
                               int num_particles)
    : estimator(estimator) {
    this->judge = judge;
    this->sds_estimating = this->estimator.sds_estimating;
    this->sds_using = this->estimator.sds_using;
    this->past_sds_using = this->estimator.past_sds_using;
    this->gen = std::default_random_engine(get_rand_seed());
    this->distribution = std::uniform_real_distribution<double>(0.0, 1.0);
    this->num_particles = num_particles;
    // Here we do not trim down the past states of starting state to only have
    // past_sds_using because that would not change the amount we are
    // storing or copying
    particle starting_particle =
        particle(std::shared_ptr<RobotStateHistory>(
                     new RobotStateHistory(starting_state)),
                 1.);
    this->particles.push_back(starting_particle);
    std::unordered_set<SD> all_sds_to_keep = sds_using;
    for (SD sd : past_sds_using) {
        all_sds_to_keep.insert(sd);
    }
    starting_particle.state_history->trim_to(all_sds_to_keep);
}

RobotStateHistory ParticleFilter::updateState(RobotStateHistory state_history,
                                              RobotState new_state) {
    state_history.add_state(new_state);
    RobotState update =
        this->estimator.f(state_history.trimmed_copy(this->sds_using), true);
    state_history.use_all(update);
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

void ParticleFilter::addState(RobotState new_state, RobotState previous_state) {
    // Creates a vector if update state histories
    previous_state.trim_to(this->past_sds_using);
    for (particle particle : this->particles) {
        particle.state_history->current_state->use_extras(previous_state);
    }
    new_state.trim_to(this->sds_using);
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
    if (state.get_size() == 1) {
        this->addState(state.get_current_state());
    } else {
        this->addState(state.get_current_state(),
                       state.states_ago_trimmed(1, this->past_sds_using));
    }
    return this->getState();
}

std::shared_ptr<StateEstimator> ParticleFilter::getStateEstimator() {
    auto f = [this](RobotStateHistory state_history,
                    bool with_uncertianity) mutable -> RobotState {
        return this->estimate(state_history);
    };
    return std::shared_ptr<StateEstimator>(new StateEstimator(
        f, this->past_sds_using, this->sds_using, this->sds_estimating));
}
