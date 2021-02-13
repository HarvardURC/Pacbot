const double MILLIS_TO_SECCS = 1000;
double millis_to_secs(int millis) { return millis * MILLIS_TO_SECCS; }
double secs_to_millis(int secs) { return secs / MILLIS_TO_SECCS; }