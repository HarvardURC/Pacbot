#ifndef DEQUE_H
#define DEQUE_H

#include <iterator>
#include <vector>

// For some reason this is fucked
template <typename T> class Deque {
  private:
    std::vector<T> data;
    int max_size;
    int first_index;
    int last_index;
    int normalize_index(int index);
    int get_real_index(int eff_index);
    int get_eff_index(int real_index);
    int shift_index(int index, bool inc_index);
    bool index_in_bounds(int eff_index);

  public:
    Deque();
    Deque(int max_size);
    int length();
    int get_max_size();
    void set_max_size(int max_size);
    T get(int index);
    T last();
    void set(int index, T el);
    void add(T el);
    void add_to_end(T el);
    T pop_first();
    T pop_last();
    Deque<T> clone();
};

#endif