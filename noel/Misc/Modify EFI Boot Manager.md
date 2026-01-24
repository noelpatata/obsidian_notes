List entries:
``` bash
sudo efibootmgr
```
Change boot order:
``` bash
sudo efibootmgr -o 0003,0001,0000
```
Create new entry:
``` bash
sudo efibootmgr --create --disk /dev/sda --part 1 --loader /EFI/GRUB/grubx64.efi --label "GRUB" --verbose\n
```