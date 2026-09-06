#include <Arduino.h>
#include "tasks/SemaphoreControl.cpp"

// Pins
const int RED_PIN = 4;
const int ORANGE_PIN = 7;
const int GREEN_PIN = 8;

SemaphoreControl semaphoreControl(RED_PIN, ORANGE_PIN, GREEN_PIN);



void setup() {
  semaphoreControl.setup();
}

void loop() {
  semaphoreControl.loop();
}