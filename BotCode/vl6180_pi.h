#ifndef _VL6180_
#define _VL6180_


typedef int vl6180;
int read_byte(vl6180 handle, int reg);
void write_byte(vl6180 handle, int reg,char data);
void write_two_bytes(vl6180 handle, int reg,int data);
void start_range(vl6180 handle);
void poll_range(vl6180 handle, char addr) ;
void clear_interrupts(vl6180 handle) ;
void set_scaling(vl6180 handle, int new_scaling);
vl6180 vl6180_initialise(int device, int loc);	
int change_address(vl6180 handle, char new_addr);
int get_ir_distance(vl6180 handle, char addr);



#endif
