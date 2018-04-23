from low_level.motors import Motors

M = Motors()

try:
    #M.turn_left()
    M.advance(5500)

except KeyboardInterrupt:
    M.stop()
