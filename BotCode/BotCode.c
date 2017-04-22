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
#include "network.h"
#include "AStar.h"
#include "state.h"
#include "grid.h"
#include "FloodFill.h"
//#include "movement.h"
//#include <wiringPi.h>
//#include <Direction.c> 
// Initialize connection with camera
//Must have two modes 

// GLOBALS 
free_cell* grid; 
state_response* latest_state;
cell_pos *max1;
cell_pos *max2;
cell_pos *max3;

int getDirectionGhost(cell_pos* init, cell_pos* final);



int main(int argc, char **arg) {

    ghost_dir* directions = (ghost_dir*)malloc(sizeof(ghost_dir));

    //setupMovement();

    // softPwmCreate(pwmPinL, 0, 100);
    // softPwmCreate(pwmPinR, 0, 100);
    
    latest_state = malloc(sizeof(state_response));
    if(latest_state == NULL) {
        return -1;
    }
    createGrid();


    
    ghost_flood();

    cell_pos start_pos;
    cell_pos goal_pos;
    start_pos.cp_x = 1;
    start_pos.cp_y = 1;
    goal_pos.cp_x = 29;
    goal_pos.cp_y = 26;
    uint8_t actionbuffer[200];

    int test = getActionList(start_pos, 1, goal_pos, 1, &(actionbuffer[0]));
    for(int i = 0; i < 200; i++){
        printf("%d\n", actionbuffer[i]);
    }



    for(int i =0; i<31; i++) {
        for (int j = 0; j < 28; j++)
        {
            printf("%03d ", grid[j+ i*28].ghost_danger);
        }
        printf("\n");
    }
    /*pollState();
    cell_pos blink_cur = getBlinky();
    cell_pos ink_cur = getInky();
    cell_pos pink_cur = getPinky();
    cell_pos clyde_cur = getClyde();
    state_response state;
    cell_pos blink_last;
    cell_pos ink_last;
    cell_pos pink_last;
    cell_pos clyde_last;
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

        if (getDirectionGhost(*blink_last, *blink_cur) != 0){
            directions->blink_dir = getDirectionGhost(*blink_last, *blink_cur);
            directions->ink_dir = getDirectionGhost(*ink_last, *ink_cur);
            directions->pink_dir = getDirectionGhost(*pink_last, *pink_cur);
            directions->clyde_dir = getDirectionGhost(*clyde_last, *clyde_cur);
        }

        //call flood then immediately a*
        (directions);

    }*/
        
    free(grid);
    return 0; 
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