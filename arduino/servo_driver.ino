#include <Servo.h>

Servo servo;
const int servoPin = 9;

void setup() {
  Serial.begin(115200);
  servo.attach(servoPin);
  servo.write(90);
  delay(500);
  Serial.println("Ready");
}

void loop() {
  if (Serial.available()) {
    String line = Serial.readStringUntil('\n');
    line.trim();

    if (line.length() > 0) {
      int angle = line.toInt();
      angle = constrain(angle, 0, 180);

      servo.write(angle);
      Serial.println(angle);
    }
  }
}
