#ifndef DEQUE
#define DEQUE

#include "../utils/number_manipulation.hpp"
#include <iterator>
#include <stdio.h>
#include <string>
#include <vector>

template <typename T> class Deque {
  private:
    std::vector<T> data;
    int max_size;
    int first_index; // inclusive
    int length;
    int normalize_index(int index) const;
    int get_real_index(int eff_index) const;
    int get_eff_index(int real_index) const;
    int shift_index(int index, bool inc_index) const;
    int inc_index(int index) const;
    int dec_index(int index) const;
    bool eff_index_in_bounds(int eff_index) const;

  public:
    Deque();
    Deque(int max_size);
    int size() const;
    int get_max_size() const;
    void set_max_size(int max_size);
    T get(int index) const;
    T last() const;
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
    this->length = 0;
}

template <typename T> Deque<T>::Deque(int max_size) {
    this->max_size = max_size;
    this->first_index = -1;
    this->length = 0;
}
// eff_index = effective index
template <typename T> int Deque<T>::normalize_index(int index) const {
    if (this->max_size == 0) {
        return 0;
    } else {
        return modulo(index, this->max_size);
    }
}

// The arraylist is set up, so we add to the end
// Which means if we have the effective arraylist of [1, 2, 3], that's
// represented as [3, 2, 1, 0, 0, ..., 0]. Here the first index would be 2.
// Thus effective_index = first_index - real_index, meaning real_index =
// first_index - effective_index
template <typename T> int Deque<T>::get_real_index(int eff_index) const {
    return normalize_index(first_index - eff_index);
}
template <typename T> int Deque<T>::get_eff_index(int real_index) const {
    return normalize_index(first_index - real_index);
}
template <typename T>
int Deque<T>::shift_index(int real_index, bool inc_index) const {
    int inc_amount = inc_index ? -1 : 1;
    return normalize_index(real_index + inc_amount);
}
template <typename T> int Deque<T>::inc_index(int real_index) const {
    return this->shift_index(real_index, true);
}
template <typename T> int Deque<T>::dec_index(int real_index) const {
    return this->shift_index(real_index, false);
}
template <typename T> int Deque<T>::size() const { return this->length; }
template <typename T> int Deque<T>::get_max_size() const {
    return this->max_size;
}
template <typename T> bool Deque<T>::eff_index_in_bounds(int eff_index) const {
    return eff_index >= 0 && eff_index < this->size();
}
template <typename T> T Deque<T>::get(int eff_index) const {
    if (eff_index_in_bounds(eff_index)) {
        return this->data.at(get_real_index(eff_index));
    } else {
        throw std::out_of_range("Deque: Index = " + std::to_string(eff_index) +
                                ", Length = " + std::to_string(size()));
    }
}
template <typename T> void Deque<T>::set(int eff_index, T el) {
    if (eff_index_in_bounds(eff_index)) {
        this->data[get_real_index(eff_index)] = el;
    } else {
        throw std::out_of_range("Deque: Index = " + std::to_string(eff_index) +
                                ", Length = " + std::to_string(size()));
    }
}
template <typename T> T Deque<T>::last() const { return get(size() - 1); }
template <typename T> T Deque<T>::pop_first() {
    T val = get(0);
    // This is shifting forward because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element
    // When you pop out the 1, you need to move the pointer forward to the 2
    //    but the ' needs to stay at the 3
    this->first_index = inc_index(this->first_index);
    return val;
}
template <typename T> T Deque<T>::pop_last() {
    T val = last();
    // This is shifting backwards because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element
    // When you pop out the 3, you need to move the end pointer back to the 2
    //    and the * stays at the 1
    this->length -= 1;
    return val;
}
template <typename T> void Deque<T>::add(T el) {

    // We do dec_index(this->first_index) because let's say you have some deque
    // with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element and the ' marks the pointer to the last element
    // When you add 0, the data becomes [0, 1*, 2] 3', so you have to move
    // the star pointer one less, and same with the ' assuming the deque
    // is at max capacity
    this->length = std::min(this->length + 1, this->max_size);
    if (this->data.size() != max_size) {
        this->data.push_back(el);
        this->first_index = dec_index(this->first_index);
    } else {
        this->first_index = dec_index(this->first_index);
        this->data[this->first_index] = el;
    }
}

template <typename T> void Deque<T>::set_max_size(int max_size) {
    for (int i = this->max_size; i < max_size; i--) {
        this->pop_last();
    }
    this->max_size = max_size;
}

template <typename T> Deque<T> Deque<T>::clone() {
    Deque<T> deque = Deque(this->max_size);
    for (int i = this->size() - 1; i >= 0; i--) {
        deque.add(this->get(i));
    }
    return deque;
}

#endif
