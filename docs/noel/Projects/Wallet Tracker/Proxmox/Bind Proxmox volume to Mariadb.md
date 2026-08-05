# Create the volume
Permissions
```bash
mkdir /mnt/volume_folder
chown -R 100100:100101 /mnt/volume_folder
```
**Note**: 100 and 101 is for mysql:mysql the preffix 100 is because these are containers.
# Bind the volume
``` bash
pct set VM_ID -mp0 /proxmox/source,mp=/container/destination
```