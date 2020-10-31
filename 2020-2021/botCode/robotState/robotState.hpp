#include <exception>
#include <string>
#include <unordered_map>
#include <unordered_set>

enum SD { Row, Col, Angle };
struct SDHash {
    std::size_t operator()(SD sd) const { return (int)sd; }
};

class RobotState {

  public:
    class sd_not_found_exception : public std::exception {
      private:
        SD sd;
        std::string proc_name;

      public:
        sd_not_found_exception(const std::string proc, SD sd);
        const char *what() const throw() {
            // written like this to prevent warnings from gcc
            std::string msg =
                proc_name +
                ", referenced SD not found. Referenced SD: " + sd_to_string(sd);
            const char *real_msg = msg.c_str();
            return real_msg;
        };
    };
    RobotState(std::unordered_map<SD, double, SDHash> data);
    RobotState();

  private:
    std::unordered_map<SD, double, SDHash> data;
    static std::string sd_not_found_msg(std::string proc_name, SD sd);
    void throw_if_not_found(std::string proc_name, SD sd);

  public:
    bool contains(SD sd);
    bool get(SD sd);
    void set(SD sd, double val);
    void remove(SD sd);
    double pop(SD sd);
    std::unordered_set<SD, SDHash> get_keys();
    static std::string sd_to_string(SD sd);
    RobotState clone();
}; // namespace std