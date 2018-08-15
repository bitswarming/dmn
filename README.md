# GPU INSTALL
1. ```sudo -s```
1. ```apt install build-essential```
1. ```curl -O -L http://us.download.nvidia.com/XFree86/Linux-x86_64/390.67/NVIDIA-Linux-x86_64-390.67.run```
1. ```chmod +x NVIDIA-Linux-x86_64-390.67.run```
1. ```./NVIDIA-Linux-x86_64-390.67.run```
1. ```apt install git```
1. ```git clone https://github.com/bitswarming/dmn.git```
1. ```cd dmn```
1. ```vim .env``` #change TINCIP variable
1. ```./i.sh```

#bash <(curl -s  https://raw.githubusercontent.com/bitswarming/dmn/master/i.sh)
