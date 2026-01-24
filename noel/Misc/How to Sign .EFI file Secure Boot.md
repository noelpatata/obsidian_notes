This guide shows how to sign an .EFI file in order to enable secure boot and be able to boot your system (Minegrub in my case)
# Requirements
 ``` bash
 yay -S shim-signed sbsigntools
 ```

# Generate keys
```bash
openssl req -new -x509 -newkey rsa:2048 -keyout DB.key -out DB.crt -nodes -days 3650 -subj "/CN=MineGrub DB/"
```
Then conver to .DER format
``` bash
openssl x509 -outform DER -in DB.crt -out DB.der
``` 
# Sign .EFI file
```bash
sbsign --key DB.key --cert DB.crt --output BOOTX64.EFI /boot/EFI/BOOT/BOOTX64.EFI
```
You can also verify the signature
``` bash
sbverify --cert DB.der BOOTX64.EFI
```
# Change boot order (optional)
Generate a new entry
```bash
sudo efibootmgr -c \
  -d /dev/sda \
  -p 1 \
  -L "Minegrub" \
  -l '\EFI\BOOT\BOOTX64.EFI'
```
And change its order
```bash
sudo efibootmgr -o ID
```