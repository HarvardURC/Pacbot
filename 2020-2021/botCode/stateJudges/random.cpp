#include "random.hpp"
#include <random>

namespace RandJudge {
std::default_random_engine generator;
std::uniform_real_distribution<double> distribution(0.0, 1.0);
} // namespace RandJudge

double randomJudge(RobotStateHistory _stateHistory) {
    return RandJudge::distribution(RandJudge::generator);
}