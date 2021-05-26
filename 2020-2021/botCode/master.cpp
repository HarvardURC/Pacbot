#include "master.hpp"
#include <stdio.h>

#include "controllers/wall_follower.hpp"
#include "robotState/globalState.hpp"
#include "sensorsActuators/motors.hpp"
#include "sensorsActuators/sensors.hpp"
#include "stateEstimators/particleFilter.hpp"
#include "stateEstimators/testEstimator.hpp"
#include "stateEstimators/wheelPos.hpp"
#include "stateJudges/optimistic.hpp"
#include "stateJudges/random.hpp"
#include "stateJudges/testJudge.hpp"
// #include "wiringPi.h"
#include <chrono>
#include <thread>

std::shared_ptr<RobotStateHistory> state_history(new RobotStateHistory());
ParticleFilter *particle_filter = nullptr;
std::shared_ptr<StateEstimator> particle_filter_est = nullptr;

void on_init() {
    /* wiringPiSetup();
    initialize_motors();
    initialize_sensors();
    follower = new wall_follower(0.1, true);
    */

    state_history->set(SD::Angle, 0.0);
    printf("current val, len: %f, %d\n", state_history->get(SD::Angle),
           state_history->get_size());

    particle_filter =
        new ParticleFilter(getTestEstimator(), test_judge, *state_history);
    particle_filter_est = particle_filter->getStateEstimator();
}
void on_periodic(bool *is_running) {
    state_history->add_empty_state();
    particle_filter_est->apply(state_history);
    printf("current val, len: %f, %d\n", state_history->get(SD::Angle),
           state_history->get_size());
    *is_running = false;
}
void loop() {
    bool is_running_val = true;
    bool *is_running = &is_running_val;
    *is_running = true;
    std::thread th(on_periodic, std::ref(is_running));
    std::this_thread::sleep_for(
        std::chrono::milliseconds((int)secs_to_millis(TICK_LENGTH)));
    // Ideally this is_running system should be changed to actually check if the
    //    thread finishes
    // th.join();
    if (*is_running) {
        printf(
            "\n WARNING: on_periodic is taking longer than the TICK_LENGTH of "
            "%d milliseconds.\n",
            (int)secs_to_millis(TICK_LENGTH));
        th.join();
        printf("Loop continuing.\n");
    } else {
        th.join();
    }
    loop();
}

void start() {
    on_init();
    loop();
}

int main() { start(); }
