#include "master.hpp"
#include <stdio.h>

#include "controllers/wall_follower.hpp"
#include "robotState/globalState.hpp"
#include "sensorsActuators/motors.hpp"
#include "sensorsActuators/sensors.hpp"
#include "stateEstimators/wheelPos.hpp"
// #include "wiringPi.h"
#include <chrono>
#include <thread>

wall_follower *follower = nullptr;
void on_init() {
    // wiringPiSetup();
    initialize_motors();
    initialize_sensors();
    follower = new wall_follower(0.1, true);
    auto _a = getWheelPosEstimator();
    return;
}
void on_periodic(bool *is_running) {
    follower->update();
    *is_running = true;
}
void loop() {
    bool *is_running = (bool *)malloc(1);
    *is_running = true;
    std::thread th(on_periodic, std::ref(is_running));
    std::this_thread::sleep_for(
        std::chrono::milliseconds((int)secs_to_millis(TICK_LENGTH)));
    // Ideally this is_running system should be changed to actually check if the
    //    thread finishes
    th.join();
    if (*is_running) {
        printf(
            "\n WARNING: on_periodic is taking longer than the TICK_LENGTH of "
            "%d milliseconds.\n",
            (int)secs_to_millis(TICK_LENGTH));
        // th.join();
        printf("Loop continuing.\n");
    } else {
        // th.join();
    }
    loop();
}

void start() {
    on_init();
    loop();
}

int main() { start(); }
