#include <Arduino.h>
#include "DebouncedButton.hpp"

// Pins
const int LED_PIN = 4;
const int BUTTON_PIN = 2;

DebouncedButton button(BUTTON_PIN);


void setup() {
  pinMode(LED_PIN, OUTPUT);
  button.begin(INPUT);
}

void loop() {

  if(button.wasPressed()){
    digitalWrite(LED_PIN, !digitalRead(LED_PIN));
  }
  
}