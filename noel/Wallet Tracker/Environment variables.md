# windows
``` bash
setx WALLET_TRACKER_DB_USER root 
setx WALLET_TRACKER_DB_PASSWORD adminadmin
setx WALLET_TRACKER_DB_HOST 127.0.0.1
setx WALLET_TRACKER_DB_NAME wallet_tracker
setx WALLET_TRACKER_SECRET s0m3r4nd0mt3xt
```
# linux
``` bash
echo 'export WALLET_TRACKER_DB_USER=root' >> ~/.bashrc && \
echo 'export WALLET_TRACKER_DB_PASSWORD=adminadmin' >> ~/.bashrc && \
echo 'export WALLET_TRACKER_DB_HOST=127.0.0.1' >> ~/.bashrc && \
echo 'export WALLET_TRACKER_DB_NAME=wallet_tracker' >> ~/.bashrc && \
echo 'export WALLET_TRACKER_SECRET=s0m3r4nd0mt3xt' >> ~/.bashrc
```