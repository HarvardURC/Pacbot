/* Encoder Library - TwoKnobs Example
 * http://www.pjrc.com/teensy/td_libs_Encoder.html
 *
 * This example code is in the public domain.
 */

#include <Encoder.h>

// Change these pin numbers to the pins connected to your encoder.
//   Best Performance: both pins have interrupt capability
//   Good Performance: only the first pin has interrupt capability
//   Low Performance:  neither pin has interrupt capability
Encoder knobLeft(2, 3);
Encoder knobRight(14, 15);
//   avoid using pins with LEDs attached

void setup() {
  Serial1.setTX(1);
  Serial1.setRX(2);
  Serial1.begin(9600);
  Serial.begin(9600);
  Serial1.println("TwoKnobs Encoder Test:");
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
