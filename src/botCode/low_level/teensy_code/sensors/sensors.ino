/* 
 * Code for interfacing with encoders and IMU from Teensy.
 * 
 * Encoder code is from this tutorial:
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 * 
 */

#include <Encoder.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>


/* Set the delay between fresh samples */
#define SAMPLERATE_DELAY_MS (50)

/* Set up Encoder */
// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder knobLeft(2, 3);
Encoder knobRight(14, 15);
//   avoid using pins with LEDs attached


/* Set up IMU */

// A few notes from Tom:
// - we were using the wrong I2C bus - the IMU was hooked up to Wire1. This requires changing the Wire library so that Wire1 is defined. Specifically, uncomment #define WIRE_IMPLEMENT_WIRE1 in WireKinetis.h
// - also the sensors need to be calibrated. This website has info for how to do that: https://learn.adafruit.com/adafruit-bno055-absolute-orientation-sensor/device-calibration 

// Check I2C device address and correct line below (by default address is 0x29 or 0x28), make sure the bus is ok too!
//                                   id, address
Adafruit_BNO055 bno = Adafruit_BNO055(-1, 0x28, &Wire1);


/* Print to one serial bus */
auto CurrSerial = Serial1;

void setup() {
  delay(10000);           // teensy was turning on too fast
  CurrSerial.begin(38400);

  /* Initialise the IMU */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    CurrSerial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }

  delay(1000);

  bno.setExtCrystalUse(true);
}

long positionLeft  = -999;
long positionRight = -999;

String printVectorValues(imu::Vector<3> vector) {
  return String(vector.x()) + " " + String(vector.y()) + " " + String(vector.z()) + "\t";
}

void loop() {

  // Base string
  String base = "";
  
  /*
   * Encoder reading and writing
   * 
   */
  // if a character is sent from the CurrSerial monitor,
  // reset both back to zero.
  if (CurrSerial.available()) {
    CurrSerial.read();
    knobLeft.write(0);
    knobRight.write(0);
  }
  
  long newLeft, newRight;
  newLeft = knobLeft.read();
  newRight = knobRight.read();
  base += String(newLeft);
  base += " ";
  base += String(newRight);
  
  base += "\t";


  /*
   * IMU reading and writing
   * 
   */
   
  // Possible vector values can be:
  // - VECTOR_ACCELEROMETER - m/s^2
  // - VECTOR_MAGNETOMETER  - uT
  // - VECTOR_GYROSCOPE     - rad/s
  // - VECTOR_EULER         - degrees
  // - VECTOR_LINEARACCEL   - m/s^2
  // - VECTOR_GRAVITY       - m/s^2
//  imu::Vector<3> accelerometer = bno.getVector(Adafruit_BNO055::VECTOR_LINEARACCEL);
//  //  base += "LINEARACCEL: ";
//  base += printVectorValues(accelerometer);
//
//  imu::Vector<3> gyroscope = bno.getVector(Adafruit_BNO055::VECTOR_GYROSCOPE);
//  //  base += "GYROSCOPE: ";
//  base += printVectorValues(gyroscope);

  imu::Vector<3> euler = bno.getVector(Adafruit_BNO055::VECTOR_EULER);
  //  base += "EULER: ";
  base += printVectorValues(euler);
  

  /* Display calibration status for each sensor. */
//  uint8_t system, gyro, accel, mag = 0;
//  bno.getCalibration(&system, &gyro, &accel, &mag);
//  //  base += "CALIBRATION: Sys=";
//  base += String(system);
//  //  base += " Gyro=";
//  base += String(gyro);
//  //  base += " Accel=";
//  base += String(accel);
//  //  base += " Mag=";
//  base += String(mag);

  CurrSerial.println(base);

  delay(SAMPLERATE_DELAY_MS);
}
