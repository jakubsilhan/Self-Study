#include <Arduino.h>

class SemaphoreControl {
public:
    SemaphoreControl(int redPin, int yellowPin, int greenPin)
        : redPin(redPin), yellowPin(yellowPin), greenPin(greenPin) {}

    void setup() {
        pinMode(redPin, OUTPUT);
        pinMode(yellowPin, OUTPUT);
        pinMode(greenPin, OUTPUT);
    }

    void loop() {
        set_led_states(RED);
        delay(3000);
        set_led_states(RED_ORANGE);
        delay(1000);
        set_led_states(GREEN);
        delay(3000);
        set_led_states(ORANGE);
        delay(1000);
    }

private:
    const int redPin;
    const int yellowPin;
    const int greenPin;

    const int RED[3] = {HIGH, LOW, LOW};
    const int RED_ORANGE[3] = {HIGH, HIGH, LOW};
    const int GREEN[3] = {LOW, LOW, HIGH};
    const int ORANGE[3] = {LOW, HIGH, LOW};

    void set_led_states(const int states[3]) {
        digitalWrite(redPin, states[0]);
        digitalWrite(yellowPin, states[1]);
        digitalWrite(greenPin, states[2]);
    }
};