# First get these files
``` bash
wget https://github.com/ruvnet/RuView/releases/download/v0.5.0-esp32/bootloader.bin && \
wget https://github.com/ruvnet/RuView/releases/download/v0.5.0-esp32/esp32-csi-node.bin && \
wget https://github.com/ruvnet/RuView/releases/download/v0.5.0-esp32/partition-table.bin && \
wget https://raw.githubusercontent.com/ruvnet/RuView/main/firmware/esp32-csi-node/provision.py
```
# Create environment
``` bash
mkdir ruview_setup && \
python -m venv .venv && \
source .venv/bin/activate && \
pip install esptool pyserial esp-idf-nvs-partition-gen && \
```
# Script 
## Enter ESP32-S3 in BOOT mode
Press and hold BOOT button and then press RST button, this will enable BOOT mode, you will notice it because RGB animation will stop.
## Script prerequisites
Change permissions so the script can flash the devices
```bash
sudo usermod -a -G uucp $USER && \
sudo chmod 666 /dev/ttyACM0 && \
sudo chmod 666 /dev/ttyACM1 && \
sudo chmod 666 /dev/ttyACM2
```
## Flash
```bash
python -m esptool --chip esp32s3 --port /dev/ttyACM0 --baud 460800 \
  write-flash --flash-mode dio --flash-size 8MB --flash-freq 80m \
  0x0 bootloader.bin \
  0x8000 partition-table.bin \
  0xf000 ota_data_initial.bin \
  0x20000 esp32-csi-node.bin
```

```bash
python -m esptool --chip esp32s3 --port /dev/ttyACM1 --baud 460800 \
  write-flash --flash-mode dio --flash-size 8MB --flash-freq 80m \
  0x0 bootloader.bin \
  0x8000 partition-table.bin \
  0xf000 ota_data_initial.bin \
  0x20000 esp32-csi-node.bin
```

```bash
python -m esptool --chip esp32s3 --port /dev/ttyACM2 --baud 460800 \
  write-flash --flash-mode dio --flash-size 8MB --flash-freq 80m \
  0x0 bootloader.bin \
  0x8000 partition-table.bin \
  0xf000 ota_data_initial.bin \
  0x20000 esp32-csi-node.bin
```

## Provision
``` bash
python provision.py --port /dev/ttyACM0 \
  --ssid "$WIFI_SSID" \
  --password "$WIFI_PASSWORD" \
  --target-ip $MY_IP \
  --target-port 5005 \
  --node-id 1 \
  --tdm-slot 0 \
  --tdm-total 3 \
  --edge-tier 2 \
  --pres-thresh 40 \
  --fall-thresh 15000 \
  --vital-win 300 \
  --vital-int 500 \
  --subk-count 32 && \
python provision.py --port /dev/ttyACM1 \
  --ssid "$WIFI_SSID" \
  --password "$WIFI_PASSWORD" \
  --target-ip $MY_IP \
  --target-port 5005 \
  --node-id 2 \
  --tdm-slot 1 \
  --tdm-total 3 \
  --edge-tier 2 \
  --pres-thresh 40 \
  --fall-thresh 15000 \
  --vital-win 300 \
  --vital-int 500 \
  --subk-count 32 && \
python provision.py --port /dev/ttyACM2 \
  --ssid "$WIFI_SSID" \
  --password "$WIFI_PASSWORD" \
  --target-ip $MY_IP \
  --target-port 5005 \
  --node-id 3 \
  --tdm-slot 2 \
  --tdm-total 3 \
  --edge-tier 2 \
  --pres-thresh 40 \
  --fall-thresh 15000 \
  --vital-win 300 \
  --vital-int 500 \
  --subk-count 32
```

  

# Run
``` bash
docker run --name ruview-mesh -p 3000:3000 -p 3001:3001 -p 5005:5005/udp -e CSI_SOURCE=esp32 ruvnet/wifi-densepose:latest
```