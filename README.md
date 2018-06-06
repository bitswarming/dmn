# dmn
sudo -s

apt install build-essential
curl -O -L http://us.download.nvidia.com/XFree86/Linux-x86_64/390.67/NVIDIA-Linux-x86_64-390.67.run

chmod +x NVIDIA-Linux-x86_64-390.67.run 

./NVIDIA-Linux-x86_64-390.67.run 

bash <(curl -s  https://raw.githubusercontent.com/bitswarming/dmn/master/i.sh)
