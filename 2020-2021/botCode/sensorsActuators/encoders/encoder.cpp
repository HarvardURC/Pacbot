
// C library headers
#include <stdio.h>
#include <string.h>

// Linux headers
#include "rs232.h"
#include <errno.h>   // Error integer and strerror() function
#include <fcntl.h>   // Contains file controls like O_RDWR
#include <termios.h> // Contains POSIX terminal control definitions
#include <unistd.h>  // write(), read(), close()
class Encoders {
  public:
    int size = 1;
    // mode is 8N1?

    int cport_nr = 0;  /* /dev/ttyS0 (COM1 on windows) */
    int bdrate = 9600; /* 9600 baud */

    unsigned char buf[4096];

    char mode[4] = {'8', 'N', '1', (char)0};

    void update() {

        int ser = RS232_OpenComport(cport_nr, bdrate, mode,
                                    0); // opens the serial port?
        usleep(100000);
        RS232_SendByte(cport_nr, 'a');
        usleep(100000);
        int curpos = 0;

        while (true) {

            int n = RS232_PollComport(cport_nr, &(buf[curpos]),
                                      size); // get the numbers from the port
            if (n == 1) {
                if (buf[curpos] == '\n') {
                    buf[curpos + 1] = 0;
                    printf("%s", buf);
                    curpos = 0;
                } else {
                    curpos++;
                }
            }
        }
        RS232_CloseComport(cport_nr); // close the comport maybe?
    }
};

int main(void) {
    printf("hello world\n");
    Encoders measure;
    measure.update();
}
