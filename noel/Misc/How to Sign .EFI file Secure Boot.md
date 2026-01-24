This guide shows how to sign an .EFI file in order to enable secure boot and be able to boot your system (Minegrub in my case)
# Requirements
 ``` bash
 yay -S sbctl
 ```

# Enter Setup Mode
This section basically means to disable secure boot and remove vendor default keys.
# Enroll key
Create
``` bash
sbctl create-keys
```
And enroll
``` bash
sudo sbctl enroll-keys -m
```
# Sign .EFI file
```bash
sudo sbctl sign -s /boot/vmlinuz-linux
```

Choose the .efi you use to boot the system.
```bash
sudo sbctl sign -s /boot/EFI/BOOT/grubx64.efi
```
# After signing

##  Automatic boot
Generate a new entry
```bash
sudo efibootmgr -c \
  -d /dev/sda \
  -p 1 \
  -L "Minegrub" \
  -l '\EFI\BOOT\grubx64.efi'
```
And change its order
```bash
sudo efibootmgr -o ID
```
## Enable secure boot
Just reboot, enable secure boot and you good to go.