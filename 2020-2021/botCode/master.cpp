#include "master.hpp"
#include <stdio.h>

/*#include "robotState/globalState.hpp"
#include <chrono>
#include <thread>

void on_init() { return; }
void on_periodic(bool *is_running) { *is_running = false; }
void loop() {
    bool *is_running = (bool *)malloc(1);
    *is_running = true;
    std::thread th(on_periodic, std::ref(is_running));
    std::this_thread::sleep_for(
        std::chrono::milliseconds((int)secs_to_millis(TICK_LENGTH)));
    // Ideally this is_running system should be changed to actually check if the
    //    thread finishes
    if (is_running) {
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
*/

int main() { throw 20; }