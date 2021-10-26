/*
  Generic arcade stick controller for Arduino Leonardo.

  Created 25 Oct 2021
  Modified 25 Oct 2021
  by Kari Suominen
*/

#include "Profiles/Profiles.h"
#define PROFILE ZXCV //The default profile which to fall back to when clearing EEPROM. Either ZXCV, ZXAS, AMOGUS or VPINBALL
char pins [] = {2,3,4,7,6,5,10,14,15,16}; //Change order if your physical setup is different, by default goes through buttons 1-6, then right, up, down, left
#define UPDATE_MS 8 //Polling interval, 60Hz rounds to 16ms interval, so double that should be enough to eliminate aliasing

#include "Profiles/ProfilePicker.h"
#include "Button/Button.h"
#include <Keyboard.h>
#include <EEPROM.h>

char buttonMap [] = {BUTTON1, BUTTON2, BUTTON3, BUTTON4, BUTTON5, BUTTON6, RIGHT, UP, DOWN, LEFT};
const char pinLength = sizeof pins / sizeof pins[0];
Button buttons[pinLength];

void pressButton(char key) {
  Keyboard.press(key);
}

void releaseButton(char key) {
  Keyboard.release(key);
}

void updateButton(Button &button) {
  if (button.update()) {
    if (button.get()) {
      pressButton(button.key);
    } else {
      releaseButton(button.key);
    }
  }
}

void setBinding(char *bindings, bool save) {
  for (char i=0; i<pinLength; i++) {
    buttons[i].set(bindings[i]);
    if (save) {
      EEPROM.write(i, bindings[i]);
    }
  }
}

//receives new bindings as bytes, expects a message 10+EOL characters long
void updateBindings() {
  if (!Serial.available()) return;

  char msg[pinLength];
  char i = 0;
  char lastChar = -1;
  while(Serial.available() && lastChar != 10) {
    lastChar = Serial.read();
    if (i < pinLength) {
      if (lastChar != 10) {
        msg[i] = lastChar;
        i++;
      }
    }
  }
  if (i == 1) {
    Serial.println((int)msg[0]);
  } else if (i == 3 && msg[0] == 'C' && msg[1] == 'L' && msg[2] == 'R') {
    setBinding(buttonMap, true);
    Serial.println("bindings cleared");
  } else if (i == 3 && msg[0] == 'G' && msg[1] == 'E' && msg[2] == 'T') {
    for (char j=0; j<10; j++){
      Serial.print((int)EEPROM.read(j));
      Serial.print(" ");
    }
    Serial.println();
  } else if (i == 10) {
    setBinding(msg, true);
    Serial.println("bindings updated");
  } else {
    Serial.println((int)i);
  }
}

void loadBinding() {
  bool ok = true;
  char binding[pinLength];
  for (char i=0; i<pinLength; i++) {
    binding[i] = EEPROM.read(i);
    if (binding[i] < 32 || binding[i] > 127) {
      ok = false;
      break;
    }
  }
  if (ok) {
    setBinding(binding, false);
  } else {
    setBinding(buttonMap, true);
  }
}

void setup() {
  for (char i=0; i<pinLength; i++) {
    pinMode(pins[i], INPUT_PULLUP);
    buttons[i].init(pins[i], 'z');
  }
  loadBinding();
  Keyboard.begin();
  Serial.begin(9600);
}

void loop() {
  updateBindings();
  for (char i=0; i<pinLength; i++) {
    updateButton(buttons[i]);
  }
  delay(UPDATE_MS);
}
