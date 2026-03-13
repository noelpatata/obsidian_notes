This commands generates the key used in the CD pipeline:
``` bash
keytool -genkeypair -v \
    -keystore wallettracker.keystore \
    -alias wallettracker \
    -keyalg RSA -keysize 2048 \
    -validity 10000
```