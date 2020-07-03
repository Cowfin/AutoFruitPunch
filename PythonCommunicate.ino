#include <Servo.h>
Servo servo;

void setup() {
  servo.attach(9);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0 ) {
    if (Serial.read() == 'o') {
      servo.write(0);
      delay(75);
    }
  } else {
    servo.write(95);
  }
}
