#pragma once
#include <Arduino.h>

class DebouncedButton {
private:
    int _pin;
    int _buttonState;
    int _lastButtonState;
    unsigned long _lastDebounceTime;
    unsigned long _debounceDelay;

public:
    DebouncedButton(int pin, unsigned long debounceDelay = 50);

    void begin(int mode = INPUT);

    bool wasPressed();
};