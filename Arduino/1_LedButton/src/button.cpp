#include "DebouncedButton.hpp"

DebouncedButton::DebouncedButton(int pin, unsigned long debounceDelay) 
    : _pin(pin), 
      _buttonState(LOW), 
      _lastButtonState(LOW), 
      _lastDebounceTime(0), 
      _debounceDelay(debounceDelay) {
}

void DebouncedButton::begin(int mode){
    pinMode(_pin, mode);
}

bool DebouncedButton::wasPressed(){
    int reading = digitalRead(_pin);
    bool pressed = false;

    if(reading!=_lastButtonState){
        _lastDebounceTime = millis();
    }

    if((millis()-_lastDebounceTime) >= _debounceDelay){
        if (reading!=_buttonState){
            _buttonState = reading;

            if (_buttonState){
                pressed = true;
            }
        }
    }

    _lastButtonState = reading;

    return pressed;
}