git clone https://github.com/bitswarming/dmn.git
cd dmn
echo "1. install recent nvidia driver http://www.nvidia.com/Download/index.aspx?lang=en-uk"
echo "2. install"
# If you have nvidia-docker 1.0 installed: we need to remove it and all existing GPU containers
#docker volume ls -q -f driver=nvidia-docker | xargs -r -I{} -n1 docker ps -q -a -f volume={} | xargs -r docker rm -f

apt-get purge -y nvidia-docker
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add -
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-docker2
sudo pkill -SIGHUP dockerd
echo "3. install docker"
apt update
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#sudo add-apt-repository \
#   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
#   $(lsb_release -cs) \
#   stable"
#apt update
#apt-get install docker-ce
#echo "4. install docker compose"
curl -L https://github.com/docker/compose/releases/download/1.21.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
echo "5. starting verai"
docker network create jupyterhub-network
docker volume create --name=jupyterhub-data
docker volume create --name=jupyterhub-db-data
docker volume create --name sokol
#docker-compose  -f docker-compose.yml up -d
docker-compose  -f docker-compose.yml up  --build   -d
