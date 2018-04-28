from low_level.motors import Motors

M = Motors()

try:
   # M.escape()
    #M.move_cells(30)
    #M.reverse(20)
    #"""
    for i in range(1):
       # M.turn_around_r()
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
    M.move_cells(6)
    M.turn_right()
    M.move_cells(10)
    M.turn_right()
    M.move_cells(8)
    M.turn_left()
    M.move_cells(20)
    M.reverse(30)
    #"""

except KeyboardInterrupt:
    M.stop()
except:
    M.stop()
