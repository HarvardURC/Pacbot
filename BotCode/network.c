#include "network.h"
#include "state.h"

static void error(const char *msg) { perror(msg); exit(0); }

static int getResponse(char* response, size_t resLen)
{
    /* first what are we going to send and where are we going to send it? */
    int portno =        8080;
    char *host =        "192.168.0.101";
    char *message = "GET /pac-bot HTTP/1.0\r\n\r\n";

    struct hostent *server;
    struct sockaddr_in serv_addr;
    int sockfd, bytes, sent, received, total;

    /* fill in the parameters */

    /* create the socket */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) error("ERROR opening socket");

    /* lookup the ip address */
    server = gethostbyname(host);
    if (server == NULL) error("ERROR, no such host");

    /* fill in the structure */
    memset(&serv_addr,0,sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(portno);
    memcpy(&serv_addr.sin_addr.s_addr,server->h_addr,server->h_length);

    /* connect the socket */
    if (connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr)) < 0)
        error("ERROR connecting");

    /* send the request */
    total = strlen(message);
    sent = 0;
    do {
        bytes = write(sockfd,message+sent,total-sent);
        if (bytes < 0)
            error("ERROR writing message to socket");
        if (bytes == 0)
            break;
        sent+=bytes;
    } while (sent < total);

    /* receive the response */
    memset(response,0, resLen);
    total = resLen-1;
    received = 0;
    do {
        bytes = read(sockfd,response+received,total-received);
        if (bytes < 0)
            error("ERROR reading response from socket");
        if (bytes == 0)
            break;
        received+=bytes;
    } while (received < total);

    if (received == total)
        error("ERROR storing complete response from socket");

    /* close the socket */
    close(sockfd);

    /* process response */
    return 0;

}

static int parseResponse(char* response, state_response *s_resp) {
    char *inky = "ghost4";
    char *blinky = "ghost1";
    char *pinky = "ghost2";
    char *clyde = "ghost3";
    char *pacbot= "pacbot";
    char *power = "specialTimer";
    char *cur = response;
    while (*cur != '{') {
        cur++;
    }
    // find the first start
    while (*cur != '"') {
        cur++;
    }
    cur++;
    if (*cur =='s') {
        // game has stopped
        s_resp->sr_state = P_STOPPED;
        return 0;
    }
    char keyBuf[50];
    char valBuf[20];
    int x = 0;
    int y = 0;
    int readingX = 0;
    s_resp->sr_state = P_REGULAR;
    cur--;
    while(1) {
        int i = 0;
        while (*cur != '"') {
            if (*cur == '\0') {
                return 0;
            }
            cur++;
        }
        // found start
        cur++;
        while (*cur != '"') {
            keyBuf[i] = *cur;
            i++;
            cur++;
        }
        keyBuf[i] = '\0';
        i = 0; 
        if (strcmp(&keyBuf[0], power) == 0) {
            while (*cur != ' ') {
                cur++;
            }
            cur++;
            while (*cur != ' ' && *cur != '\n') {
                valBuf[i] = *cur;
                cur++;
                i++;
            }
            valBuf[i] = '\0';
            s_resp->sr_power_counter = atoi(&valBuf[0]);
            s_resp->sr_state = P_POWER;
        } else {
            cur++;
            while (*cur != '"') {
                cur++;
            }
            cur++;
            if (*cur == 'x') {
                readingX = 1;
            } else {
                readingX = 0;
            }
            while (*cur != ' ') {
                cur++;
            }
            cur++;
            while (*cur != ' ' && *cur != '\n' && *cur != ',') {
                valBuf[i] = *cur;
                cur++;
                i++;
            }
            valBuf[i] = '\0';
            if(readingX) {
                x = atoi(&valBuf[0]);
            } else {
                y = atoi(&valBuf[0]);
            }
            
            while (!(*(cur-1) == ':' && *cur == ' ')) {
                cur++;
            }
            i = 0;
            cur++;
            while (*cur != ' ' && *cur != '\n' && *cur != ',') {
                valBuf[i] = *cur;
                cur++;
                i++;
            }
            valBuf[i] = '\0';
            if(readingX) {
                y = atoi(&valBuf[0]);
            } else {
                x = atoi(&valBuf[0]);
            }

            if (strcmp(&keyBuf[0], inky) == 0) {
                (&s_resp->sr_inky)->cp_x = x;
                (&s_resp->sr_inky)->cp_y = y;
            } else if (strcmp(&keyBuf[0], blinky) == 0) {
                (&s_resp->sr_blinky)->cp_x = x;
                (&s_resp->sr_blinky)->cp_y = y;
            } else if (strcmp(&keyBuf[0], pinky) == 0) {
                (&s_resp->sr_pinky)->cp_x = x;
                (&s_resp->sr_pinky)->cp_y = y;
            } else if (strcmp(&keyBuf[0], clyde) == 0) {
                (&s_resp->sr_clyde)->cp_x = x;
                (&s_resp->sr_clyde)->cp_y = y;
            } else if (strcmp(&keyBuf[0], pacbot) == 0) {
                (&s_resp->sr_pacbot)->cp_x = x;
                (&s_resp->sr_pacbot)->cp_y = y;
            }
        }
    }
    return 0;
}

int getState(state_response *state) {
    int err;
    char response[4096];
    err = getResponse(&response[0], 4096);
    if (err)  return err;
    memset(state, 0, sizeof(state_response));
    parseResponse(&response[0], state);
    return 0;
}

void pollState() {
    state_response new_state;
    int err = getState(&new_state);
    if (err)  return;
    *latest_state = new_state;
}


void printState(state_response *state) {
    printf("inky:\n\tx:%d\n\ty:%d\n", state->sr_inky.cp_x, state->sr_inky.cp_y);
    printf("blinky:\n\tx:%d\n\ty:%d\n", state->sr_blinky.cp_x, state->sr_blinky.cp_y);
    printf("pinky:\n\tx:%d\n\ty:%d\n", state->sr_pinky.cp_x, state->sr_pinky.cp_y);
    printf("clyde:\n\tx:%d\n\ty:%d\n", state->sr_clyde.cp_x, state->sr_clyde.cp_y);
    printf("pacbot:\n\tx:%d\n\ty:%d\n", state->sr_pacbot.cp_x, state->sr_pacbot.cp_y);
    printf("power: %d\n", state->sr_power_counter);
    switch (state->sr_state) {
        case P_REGULAR:
            printf("state: Regular\n");
            break;
        case P_POWER:
            printf("state: Powered\n");
            break;
        case P_STOPPED:
            printf("state: Stopped\n");
            break;
    }
}
