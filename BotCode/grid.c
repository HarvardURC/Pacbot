#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include "grid.h"
#include "state.h"

void createGrid(){
	grid = (free_cell*) malloc(868*sizeof(free_cell)); 
    FILE *fp;
    int a; 
    int b; 
    char c;  
    fp = fopen("freespaces.txt", "r"); // I open the file to read it("r")
    while(fscanf (fp, "%d,%d,%c", &a, &b, &c)==3) {  
    	free_cell new_cell; 
    	new_cell.coordinates.cp_x = a; 
    	new_cell.coordinates.cp_y = b;
    	new_cell.pacman_pos = 0; 
    	new_cell.ghost_danger = 255; 
    	new_cell.food_opt = c; 
    	new_cell.adj_cell[0].cp_x = a - 1; 
    	new_cell.adj_cell[0].cp_y = b; 
        new_cell.adj_cell[1].cp_x = a; 
        new_cell.adj_cell[1].cp_y = b + 1; 
        new_cell.adj_cell[2].cp_x = a + 1; 
        new_cell.adj_cell[2].cp_y = b; 
        new_cell.adj_cell[3].cp_x = a; 
        new_cell.adj_cell[3].cp_y = b - 1;   
    	new_cell.directions[0]= 0;
    	new_cell.directions[1]= 0; 
    	*(grid+b + 28*a) = new_cell;     
    }  

}


