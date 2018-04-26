from low_level.motors import Motors

M = Motors()

try:
    #M.move_cells(4)
    #"""
    for i in range(3):
        #M.turn_around_r()
        #M.reverse(4)
        #M.move_cells(4)
        #M.turn_around_l()
        M.move_cells(4)
        M.turn_left()
        M.move_cells(5)
        M.turn_around_l()
        M.move_cells(11)
        M.turn_right()
        M.move_cells(4)
        M.turn_right()
        M.move_cells(6)
        M.turn_right()
    #"""

except KeyboardInterrupt:
    M.stop()
except:
    M.stop()
