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

RobotStateHistory state_history;
ParticleFilter *filter = nullptr;

void on_init() {
    /* wiringPiSetup();
    initialize_motors();
    initialize_sensors();
    follower = new wall_follower(0.1, true);
    */

    state_history.set(SD::Angle, 0.0);
    filter = new ParticleFilter(getTestEstimator(), test_judge, state_history);
}
void on_periodic(bool *is_running) {
    filter->addState(RobotState());
    printf("current val: %f\n", filter->getState().get(SD::Angle));
    *is_running = false;
}
void loop() {
    bool *is_running = (bool *)malloc(1);
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
