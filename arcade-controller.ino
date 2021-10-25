/*
  Generic arcade stick controller for Arduino Leonardo.

  Created 25 Oct 2021
  Modified 25 Oct 2021
  by Kari Suominen
*/

#include "Profiles/Profiles.h"
#define PROFILE ZXCV //Either ZXCV, ZXAS, AMOGUS or VPINBALL
char pins [] = {2,3,4,5,6,7,10,14,15,16}; //Change order if your physical setup is different, by default goes through buttons 1-6, then right, up, down, left

#include "Profiles/ProfilePicker.h"
#include "Button/Button.h"
#include <Keyboard.h>

#define UPDATE_MS 8

char buttonMap [] = {BUTTON1, BUTTON2, BUTTON3, BUTTON4, BUTTON5, BUTTON6, RIGHT, UP, DOWN, LEFT};
const char pinLength = sizeof pins / sizeof pins[0];
Button buttons[pinLength];

void setup() {  
  for (char i=0; i<pinLength; i++){
    pinMode(pins[i], INPUT_PULLUP);
    buttons[i].init(pins[i], buttonMap[i]);
  }
  Keyboard.begin();
}

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

void loop() {
  for (char i=0; i<pinLength; i++) {
    updateButton(buttons[i]);
  }
  delay(UPDATE_MS);
}
