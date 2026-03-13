# Requirements
- Arduino IDE installed
- Libraries installed
- Board configured
- VSCode "Arduino Community Edition" extension
## Arduino Community Edition configuration

You need to select the board, and set the USB Port (bottom right):
![[20250621144151.png]]

## .vscode/arduino.json

it is important to indicate the "output" (upload works)

``` json
{

"configuration": "xtal=80,vt=flash,exception=disabled,stacksmash=disabled,ssl=all,mmu=3232,non32xfer=fast,eesz=4M2M,led=2,ip=lm2f,dbg=Disabled,lvl=None____,wipe=none,baud=115200",

"board": "esp8266:esp8266:nodemcuv2",

"port": "/dev/ttyUSB0",

"sketch": "NFCheckin_Reader.ino",

"output": "./.build/NFCheckin_Reader.ino.bin"

}
```