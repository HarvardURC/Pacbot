#include "master.hpp"
#include <chrono>
#include <thread>

double Master::TICK_LENGTH = millis_to_secs(20);

void Master::on_init() { return; }
void Master::on_periodic() { return; }
void Master::loop() {
    Master::on_periodic();
    std::this_thread::sleep_for(
        std::chrono::milliseconds((int)secs_to_millis(TICK_LENGTH)));
    Master::loop();
}

void Master::start() {
    Master::on_init();
    Master::loop();
}