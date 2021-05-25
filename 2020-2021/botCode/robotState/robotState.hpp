#ifndef ROBOT_STATE_H
#define ROBOT_STATE_H

#include <exception>
#include <optional>
#include <string>
#include <unordered_map>
#include <unordered_set>

enum SD { Row, Col, X, Y, LW_change, RW_change, LW_pos, RW_pos, Angle, Time };
struct SDHash {
    std::size_t operator()(SD sd) const { return (int)sd; }
};

typedef std::unordered_map<SD, double, SDHash> data_t;

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

  private:
    std::unique_ptr<std::unordered_map<SD, double, SDHash> /**/> data;
    static std::string sd_not_found_msg(std::string proc_name, SD sd);
    void throw_if_not_found(std::string proc_name, SD sd) const;

  public:
    RobotState(data_t data);
    RobotState();
    RobotState(const RobotState &robot_state);
    RobotState &operator=(const RobotState &robot_state);
    bool contains(SD sd) const;
    double get(SD sd) const;
    std::optional<double> geto(SD sd) const;
    // Set will throw if sd already has a value
    void set(SD sd, double val);
    // Set override will not through if the given sd already has a value
    void set_override(SD sd, double val);
    void remove(SD sd);
    double pop(SD sd);
    std::unordered_set<SD, SDHash> get_keys() const;
    static std::string sd_to_string(SD sd);
    void cut_down_to(RobotState robot_state, std::unordered_set<SD> to_use);
    void use_all(RobotState robot_state);
    void use(RobotState robot_state, std::unordered_set<SD> to_use);
    void use_extras(RobotState robot_state);
    void trim_to(std::unordered_set<SD> to_keep);
    std::unordered_map<SD, double, SDHash> get_data() const;
}; // namespace std

#endif