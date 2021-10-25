/*
  Generic arcade stick controller. Work in progress.

  Created 25 Oct 2021
  Modified 25 Oct 2021
  by Kari Suominen
*/

#define UPDATE_MS 8
#define DEBUG true

char pins [] = {2,3,4,5,6,7,8,9,10,14,15,16};
int pinLength = sizeof pins / sizeof pins[0];

void setup() {
  for (int i=0; i<pinLength; i++){
    pinMode(pins[i], INPUT_PULLUP);
  }
  Serial.begin(9600);
  Serial.println("Comms ok");
}

void debug() {
  if (!DEBUG) return;
  char msg[pinLength];
  for (int i=0; i<pinLength; i++){
    msg[i] = 48;
    if (digitalRead(pins[i]) == LOW) {
      msg[i] = 49;
    }
  }
  Serial.println(msg);
}

void loop() {
  debug();
  delay(UPDATE_MS);
}
