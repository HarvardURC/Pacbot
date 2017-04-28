// Initialize libraries
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include <math.h>
#include <getopt.h>
#include <assert.h>
#include <time.h>
#include <sys/time.h>
//#include <wiringPi.h>
#include "network.h"
#include "AStar.h"
#include "state.h"
#include "grid.h"
#include "FloodFill.h"
#include "pacbot_direction.h"
#include "movement.h"
//#include "movement.h"
//
//#include <Direction.c> 
// Initialize connection with camera
//Must have two modes 

#define START_DIRECTION 4

// GLOBALS 
free_cell* grid; 
state_response* latest_state;

int getDirectionGhost(cell_pos* init, cell_pos* final);



int main(int argc, char **arg) {

    int lives = 3;

    ghost_dir* directions = (ghost_dir*)malloc(sizeof(ghost_dir));

    //softPwmCreate(pwmPinL, 0, 100);
    //softPwmCreate(pwmPinR, 0, 100);
    
    latest_state = malloc(sizeof(state_response));
    if(latest_state == NULL) {
        return -1;
    }
    createGrid();
    int direc[4];
    direc[0] = 1;
    direc[1] = 4;
    direc[2] = 3;
    direc[3] = 1;

    directions->blink_dir = direc[0];
    directions->ink_dir = direc[1];
    directions->pink_dir = direc[2];
    directions->clyde_dir = direc[3];
    ghost_flood(directions);

    cell_pos start_pos;
    cell_pos goal_pos;
    cell_pos init_pos;
    //start_pos.cp_x = 1;
    //start_pos.cp_y = 1;
    //goal_pos.cp_x = 29;
    //goal_pos.cp_y = 26;
    init_pos.cp_x = 23;
    init_pos.cp_y = 13;
    uint8_t actionbuffer[200];

    /*int test = getActionList(start_pos, 1, goal_pos, 1, &(actionbuffer[0]));
    if (test) {
        printf("failed\n");
    } else {
        int i = 0;
        while(actionbuffer[i] != 5) {
            printf("%d, ", actionbuffer[i]);
            i++;
        }
        printf("%d\n", actionbuffer[i]);
    }*/

    /*for(int i =0; i<31; i++) {
        for (int j = 0; j < 28; j++)
        {
            printf("%03d ", grid[j+ i*28].ghost_danger);
        }
        printf("\n");
    }*/
 
    pollState();
    cell_pos blink_cur = getBlinky();
    cell_pos ink_cur = getInky();
    cell_pos pink_cur = getPinky();
    cell_pos clyde_cur = getClyde();
    cell_pos pacbot_cur = getPacbot();
    cell_pos blink_last;
    cell_pos ink_last;
    cell_pos pink_last;
    cell_pos clyde_last;
    cell_pos max1;
    cell_pos max2;
    cell_pos max3;
    all_init();

    int pac_direction = START_DIRECTION;
    while(getGameStatus() != P_STOPPED) {
        blink_last = blink_cur;
        ink_last = ink_cur;
        pink_last = pink_cur;
        clyde_last = clyde_cur;
        pollState();
        blink_cur = getBlinky();
        ink_cur = getInky();
        pink_cur = getPinky();
        clyde_cur = getClyde();
        pacbot_cur = getPacbot();

        if (getDirectionGhost(&blink_last, &blink_cur) != 0){
            directions->blink_dir = getDirectionGhost(&blink_last, &blink_cur);
            directions->ink_dir = getDirectionGhost(&ink_last, &ink_cur);
            directions->pink_dir = getDirectionGhost(&pink_last, &pink_cur);
            directions->clyde_dir = getDirectionGhost(&clyde_last, &clyde_cur);
        }
        cell_pos random_cell_pos; 
        random_cell_pos.cp_x = rand() % 30; 
        random_cell_pos.cp_y = rand() % 28; 

        desired_coordinates(&max1, &max2, &max3);

        ghost_flood(directions);

        
        if (max1.cp_x != 111) {
            
            if (getActionList(pacbot_cur, pac_direction, max1, 0, &(actionbuffer[0])) == 1) {

                if (max2.cp_x != 111) {

                    if (getActionList(pacbot_cur, pac_direction, max2, 0, &(actionbuffer[0])) == 1){

                        if (max3.cp_x != 111) {

                            if (getActionList(pacbot_cur, pac_direction, max3, 0, &(actionbuffer[0])) == 1){

                                while (getActionList(pacbot_cur, pac_direction, random_cell_pos, 0, &(actionbuffer[0])) == 1) {

                                    random_cell_pos.cp_x = rand() % 30; 
                                    random_cell_pos.cp_y = rand() % 28; 

                                }
                            }
                        } else {
                            while (getActionList(pacbot_cur, pac_direction, random_cell_pos, 0, &(actionbuffer[0])) == 1) {

                                random_cell_pos.cp_x = rand() % 30; 
                                random_cell_pos.cp_y = rand() % 28; 

                            }
                        }
                    }
                } else {
                    while (getActionList(pacbot_cur, pac_direction, random_cell_pos, 0, &(actionbuffer[0])) == 1) {

                        random_cell_pos.cp_x = rand() % 30; 
                        random_cell_pos.cp_y = rand() % 28; 

                    }

                }
            }
        } else {

            while (getActionList(pacbot_cur, pac_direction, random_cell_pos, 0, &(actionbuffer[0])) == 1) {

                random_cell_pos.cp_x = rand() % 30; 
                random_cell_pos.cp_y = rand() % 28; 

            }

        }

        pac_direction = pacbot_execute(&(actionbuffer[0]), pac_direction);
    
    }

    getActionList(pacbot_cur, pacbot_execute(&(actionbuffer[0])), init_pos, 1, &(actionbuffer[0]));
    pac_direction = pacbot_execute(&(actionbuffer[0]), pac_direction); 
    while (pac_direction != START_DIRECTION){
        turn_left();
        pac_direction++;
        if (pac_direction > 4) {
            pac_direction = 1;
        }
    }
    lives--;


    if (lives == 0) {
        free(grid);
        return 0; 
    }    
}
 
int getDirectionGhost(cell_pos* init, cell_pos* final){
    int ghost_direc;

    if (init->cp_x != final->cp_x){
        if (init->cp_x < final->cp_x){
            ghost_direc = SOUTH;
        }
        else{
            ghost_direc = NORTH;
        }

    return ghost_direc;
    }
    else if (init->cp_y != final->cp_y){
        if (init->cp_y < final->cp_y){
            ghost_direc = EAST;
        }

        else{
            ghost_direc = WEST;
        }
    return ghost_direc;
    }
    else{
        return 0;
    }
}
