#include "./deque.hpp"

#include <string>
#include <vector>

int modulo(int a, int b) {
    int remainder = a % b;
    return remainder < 0 ? remainder + a : remainder;
}

// The deque works like so:
// It has a max size, and a set of elements
// When you add an element, it adds it to your elements like a stack
//     If after you addthe total number of elements currently contained in the
//     deque is greater than the the max size, the last element is removed
// There is also O(1) get(index) and pop() functionality

template <typename T> Deque<T>::Deque() { return Deque(0); }

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
    return modulo(index, data.size());
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
        return data.at(get_real_index(index));
    } else {
        throw std::out_of_range("Deque, Index = " + std::to_string(index) +
                                ", Length = " + std::to_string(length()));
    }
}
template <typename T> void Deque<T>::set(int index, T el) {
    if (index_in_bounds(index)) {
        data[get_real_index(index)] = el;
    } else {
        throw std::out_of_range("Deque, Index = " + std::to_string(index) +
                                ", Length = " + std::to_string(length()));
    }
}
template <typename T> T Deque<T>::last() { return get(length() - 1); }
template <typename T> T Deque<T>::pop() {
    T val = last();
    // This is shifting backwards because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element
    // When you pop out the 1, you need to move the pointer forward to the 2
    //    but the ' needs to stay at the 3
    this->first_index = shift_index(this->first_index, true);
    return val;
}
template <typename T> void Deque<T>::add(T el) {
    if (data.size() != max_size) {
        data.push_back(el);
    } else {
        if (length() != data.size()) {
            this->last_index = shift_index(this->last_index, false);
        }
        data[this->first_index] = el;
    }
    // This is shifting backwards because let's say you have some deque with
    //    data [1*, 2 ,3'], where the star marks the pointer to the first
    //    element and the ' marks the pointer to the last element
    // When you add 0, the data becomes [0, 1*, 2], so you have to move the
    //    star pointer one less, and same with the '
    this->first_index = shift_index(this->first_index, false);
}

template <typename T> Deque<T> Deque<T>::clone() {
    Deque<T> deque = Deque(this->max_size);
    for (int i = this->length() - 1; i >= 0; i--) {
        deque.add(this->get(i));
    }
    return deque;
}