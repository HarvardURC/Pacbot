#include "data_type_helpers.hpp"

template <class T> T cmerge(T a, T b) {
    T t(a);
    t.insert(b.begin(), b.end());
    return t;
}
