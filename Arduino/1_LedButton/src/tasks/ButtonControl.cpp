#include "DebouncedButton.hpp"

class ButtonControl {
public:
    ButtonControl(int ledPin, int buttonPin)
        : ledPin(ledPin),
          button(buttonPin) {}

    void setup() {
        pinMode(ledPin, OUTPUT);
        button.begin(INPUT);
    }

    void loop() {
        if (button.wasPressed()) {
            digitalWrite(ledPin, !digitalRead(ledPin));
        }
    }

private:
    const int ledPin;
    DebouncedButton button;
};