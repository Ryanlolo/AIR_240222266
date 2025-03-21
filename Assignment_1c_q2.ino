#include <Servo.h>

Servo panServo;
Servo tiltServo;

int panAngle = 90;
int tiltAngle = 90;

String inputString = "";
bool stringComplete = false;

void setup() { 
  panServo.attach(9);
  tiltServo.attach(10);

  Serial.begin(9600);
  inputString.reserve(64);

  panServo.write(panAngle);
  tiltServo.write(tiltAngle);
}

void loop() {
  if (stringComplete) {
    int commaIndex = inputString.indexOf(',');
    if (commaIndex > 0) {
      panAngle = inputString.substring(0, commaIndex).toInt();
      tiltAngle = inputString.substring(commaIndex + 1).toInt();

      panAngle = constrain(panAngle, 0, 180);
      tiltAngle = constrain(tiltAngle, 0, 180);

      panServo.write(panAngle);
      tiltServo.write(tiltAngle);
    }

    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    inputString += inChar;

    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}