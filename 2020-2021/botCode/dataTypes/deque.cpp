#ifndef DEQUE
#define DEQUE

#include "../utils/number_manipulation.hpp"
#include <iterator>
#include <string>
#include <vector>

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

// The deque works like so:
// It has a max size, and a set of elements
// When you add an element, it adds it to your elements like a stack
//     If after you addthe total number of elements currently contained in the
//     deque is greater than the the max size, the last element is removed
// There is also O(1) get(index) and pop() functionality

template <typename T> Deque<T>::Deque() {
    this->max_size = 0;
    this->first_index = -1;
    this->last_index = 0;
}

template <typename T> Deque<T>::Deque(int max_size) {
    this->max_size = max_size;
    this->first_index = -1;
    this->last_index = 0;
}
// eff_index = effective index
template <typename T> int Deque<T>::normalize_index(int index) {
    if (index <= 0) {
        return index;
    }
    return modulo(index, this->data.size());
}
template <typename T> int Deque<T>::get_real_index(int eff_index) {
    return normalize_index(first_index - eff_index);
}
template <typename T> int Deque<T>::get_eff_index(int real_index) {
    return normalize_index(first_index - real_index);
}
template <typename T>
int Deque<T>::shift_index(int real_index, bool inc_index) {
    int inc_amount = inc_index ? -1 : 1;
    return normalize_index(first_index + inc_amount);
}

template <typename T> int Deque<T>::length() {
    return normalize_index(get_eff_index(last_index) + 1);
}
template <typename T> int Deque<T>::get_max_size() { return this->max_size; }
template <typename T> bool Deque<T>::index_in_bounds(int eff_index) {
    return eff_index < this->length() && eff_index > 0;
}
template <typename T> T Deque<T>::get(int index) {
    if (index_in_bounds(index)) {
        return this->data.at(get_real_index(index));
    } else {
        throw std::out_of_range("Deque, Index = " + std::to_string(index) +
                                ", Length = " + std::to_string(length()));
    }
}
template <typename T> void Deque<T>::set(int index, T el) {
    if (index_in_bounds(index)) {
        this->data[get_real_index(index)] = el;
    } else {
        throw std::out_of_range("Deque, Index = " + std::to_string(index) +
                                ", Length = " + std::to_string(length()));
    }
}
template <typename T> T Deque<T>::last() { return get(length() - 1); }
template <typename T> T Deque<T>::pop_first() {
    T val = get(0);
    // This is shifting forward because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element
    // When you pop out the 1, you need to move the pointer forward to the 2
    //    but the ' needs to stay at the 3
    this->first_index = shift_index(this->first_index, true);
    return val;
}
template <typename T> T Deque<T>::pop_last() {
    T val = last();
    // This is shifting backwards because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element
    // When you pop out the 3, you need to move the end pointer back to the 2
    //    and the * stays at the 1
    this->last_index = shift_index(this->last_index, false);
    return val;
}
template <typename T> void Deque<T>::add(T el) {
    if (this->data.size() != max_size) {
        this->data.push_back(el);
    } else {
        if (length() != this->data.size()) {
            this->last_index = shift_index(this->last_index, false);
        }
        this->data[this->first_index] = el;
    }
    // This is shifting backwards because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element and the ' marks the pointer to the last element
    // When you add 0, the data becomes [0, 1*, 2] 3', so you have to move
    // the star pointer one less, and same with the ' assuming the deque
    // is at max capacity
    this->first_index = shift_index(this->first_index, false);
}

template <typename T> void Deque<T>::set_max_size(int max_size) {
    for (int i = this->max_size; i < max_size; i--) {
        this->pop_last();
    }
    this->max_size = max_size;
}

template <typename T> Deque<T> Deque<T>::clone() {
    Deque<T> deque = Deque(this->max_size);
    for (int i = this->length() - 1; i >= 0; i--) {
        deque.add(this->get(i));
    }
    return deque;
}

#endif