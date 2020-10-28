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

  public:
    Deque();
    Deque(int max_size);
    int length();
    int get_max_size();
    T get(int index);
    void add(T el);
    T pop();
};