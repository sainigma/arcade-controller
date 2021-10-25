#ifndef Button_h
#define Button_h
#include "Arduino.h"
class Button {
  public:
    void init(char _pin, char _key);
    void test();
    bool update();
    bool get();
    char key;
  private:
    char pin;
    bool state;
};

void Button::init(char _pin, char _key) {
  pin = _pin;
  key = _key;
  state = false;
  pinMode(pin, INPUT_PULLUP);
}

bool Button::update() {
  bool newState = false;
  if (digitalRead(pin) == LOW) {
    newState = true;
  }
  if (newState != state) {
    state = newState;
    return true;
  }
  return false;
}

bool Button::get() {
  return state;
}
#endif