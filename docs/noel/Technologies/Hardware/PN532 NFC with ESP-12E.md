# Requirements
## Libraries
First install AdaFruit, this library communicates with the PN532.

## Boards
Now we need to install our ESP-12E board for manipulating it.

## Setting COM Port

Pretty simple, just select the connected USB device.
## Debugging

Ctrl+Shift+M to open the serial monitor, and setting the baud rate to 115200 will allow us to read the prints that are in the code.

## Checking if board detects PN532

``` c#
#include <Wire.h>

void setup() {
  Wire.begin(D2, D1);
  Serial.begin(115200);
  Serial.println("\nI2C Scanner");
}

void loop() {
  byte error, address;
  int nDevices = 0;

  for(address = 1; address < 127; address++ ) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C device found at address 0x");
      if (address<16) Serial.print("0");
      Serial.println(address, HEX);
      nDevices++;
    }
  }
  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");

  delay(5000);
}

```