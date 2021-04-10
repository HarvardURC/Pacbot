#ifndef DEQUE
#define DEQUE

#include "../utils/number_manipulation.hpp"
#include <iterator>
#include <string>
#include <vector>
#include <stdio.h>

template <typename T> class Deque {
  private:
    std::vector<T> data;
    int max_size;
    int first_index; // inclusive
    int last_index;  // exclusive
    int normalize_index(int index);
    int get_real_index(int eff_index);
    int get_eff_index(int real_index);
    int shift_index(int index, bool inc_index);
    int inc_index(int index);
    int dec_index(int index);
    bool eff_index_in_bounds(int eff_index);

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
    this->first_index = 0;
    this->last_index = 0;
}

template <typename T> Deque<T>::Deque(int max_size) {
    this->max_size = max_size;
    this->first_index = 0;
    this->last_index = 0;
}
// eff_index = effective index
template <typename T> int Deque<T>::normalize_index(int index) {
    if (this->max_size == 0) {
        return 0;
    } else {
        return modulo(index, this->max_size);
    }
}

// The arraylist is set up, so we add to the end
// Which means if we have the effective arraylist of [1, 2, 3], that's
// represented as [0, 0, ..., 0, 3, 2, 1] Here the first index will be the final
// index in the real array If th effective index is say 1, it must clearly be
// that fnial index minus 1 hence: real_index = first_index - eff_idnex
// This also gives us: eff_idnex = first_index - real_index
template <typename T> int Deque<T>::get_real_index(int eff_index) {
    return normalize_index(first_index - eff_index);
}
template <typename T> int Deque<T>::get_eff_index(int real_index) {
    return normalize_index(first_index - real_index);
}
template <typename T>
int Deque<T>::shift_index(int real_index, bool inc_index) {
    int inc_amount = inc_index ? -1 : 1;
    return normalize_index(real_index + inc_amount);
}
template <typename T> int Deque<T>::inc_index(int real_index) {
    return this->shift_index(real_index, true);
}
template <typename T> int Deque<T>::dec_index(int real_index) {
    return this->shift_index(real_index, false);
}
template <typename T> int Deque<T>::length() {
    return normalize_index(get_eff_index(last_index));
}
template <typename T> int Deque<T>::get_max_size() { return this->max_size; }
template <typename T> bool Deque<T>::eff_index_in_bounds(int eff_index) {
    return eff_index >= 0 && eff_index < this->length();
}
template <typename T> T Deque<T>::get(int eff_index) {
    if (eff_index_in_bounds(eff_index)) {
        return this->data.at(get_real_index(eff_index));
    } else {
        throw std::out_of_range("Deque: Index = " + std::to_string(eff_index) +
                                ", Length = " + std::to_string(length()));
    }
}
template <typename T> void Deque<T>::set(int eff_index, T el) {
    if (eff_index_in_bounds(eff_index)) {
        this->data[get_real_index(eff_index)] = el;
    } else {
        throw std::out_of_range("Deque: Index = " + std::to_string(eff_index) +
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
    this->last_index = dec_index(this->last_index);
    return val;
}
template <typename T> void Deque<T>::add(T el) {
    printf("adding!!!!\n");
    if (this->data.size() != max_size) {
        this->data.push_back(el);
        this->last_index = inc_index(this->last_index);
    } else {
        if (length() == this->data.size()) {
            // The last index is decremented because now the last one is the
            // previous one
            this->last_index = dec_index(this->last_index);
	}

        // This is shifting backwards because let's say you have some deque with
        //    data [1*, 2 ,3'], where the star marks the pointer to the first
        //    element and the ' marks the pointer to the last element
        // When you add 0, the data becomes [0, 1*, 2] 3', so you have to move
        // the star pointer one less, and same with the ' assuming the deque
        // is at max capacity
        this->first_index = dec_index(this->first_index);
        
	this->data[this->first_index] = el;
	printf("Last Index: %d", this->last_index);
    }
    printf("Actual last: %d", this->last_index);
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
