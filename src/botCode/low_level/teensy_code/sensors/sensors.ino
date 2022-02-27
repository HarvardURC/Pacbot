/* 
 * Code for interfacing with encoders and IMU from Teensy.
 * 
 * Encoder code is from this tutorial:
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 * 
 */

#include <Encoder.h>

// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder knobLeft(2, 3);
Encoder knobRight(14, 15);
//   avoid using pins with LEDs attached


/* Set up IMU */
/* Set the delay between fresh samples */
#define BNO055_SAMPLERATE_DELAY_MS (100)

// A few notes from Tom:
// - we were using the wrong I2C bus - the IMU was hooked up to Wire1. This requires changing the Wire library so that Wire1 is defined. Specifically, uncomment #define WIRE_IMPLEMENT_WIRE1 in WireKinetis.h
// - also the sensors need to be calibrated. This website has info for how to do that: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/device-calibration 

// Check I2C device address and correct line below (by default address is 0x29 or 0x28), make sure the bus is ok too!
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28, &Wire1);


/* Print to one serial bus */
#define CURR_SERIAL SERIAL

void setup() {
  Serial1.setTX(1);
  Serial1.setRX(2);
  Serial1.begin(9600);
  Serial.begin(9600);
  Serial1.println("TwoKnobs Encoder Test:");


  Serial.begin(115200);
  Serial.println("Orientation Sensor Raw Data Test"); Serial.println("");

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  /* Display the current temperature */
  int8_t temp = bno.getTemp();
  Serial.print("Current Temperature: ");
  Serial.print(temp);
  Serial.println(" C");
  Serial.println("");

  bno.setExtCrystalUse(true);

  Serial.println("Calibration status values: 0=uncalibrated, 3=fully calibrated");
}

long positionLeft  = -999;
long positionRight = -999;

void loop() {
  long newLeft, newRight;
  newLeft = knobLeft.read();
  newRight = knobRight.read();
  if (newLeft != positionLeft || newRight != positionRight) {
    Serial1.print("Left = ");
    Serial1.print(newLeft);
    Serial1.print(", Right = ");
    Serial1.print(newRight);
    Serial1.println();
    positionLeft = newLeft;
    positionRight = newRight;
  }
  // if a character is sent from the Serial1 monitor,
  // reset both back to zero.
  if (Serial1.available()) {
    Serial1.read();
    Serial1.println("Reset both knobs to zero");
    knobLeft.write(0);
    knobRight.write(0);
  }
}
