#!/bin/bash
apt update
apt install -y git vim moreutils jq iputils-ping curl python3-pip ssh
export VERAI_DAEMON_HOST=172.21.0.1
mkdir -p /opt/VerAI
cd /opt/VerAI
#export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:/opt/VerAI/lib:${LD_LIBRARY_PATH}
curl -O -L https://www.dropbox.com/s/bcm26wa457i5mam/release.tar.gz?dl=0  &&  tar xzvf release.tar.gz?dl=0
cd /usr/local/bin && ln -sf /opt/VerAI/bin/VerAI ./verai
cd /opt/VerAI
jq '.daemon.uuid  = "'${DAEMONUUID}'"' daemon.cfg | sponge daemon.cfg
jq '.daemon.key  = "'${KEY}'"' daemon.cfg | sponge daemon.cfg
jq '.nats_server.domain  = "'${SERVERDOMAIN}'"' daemon.cfg | sponge daemon.cfg
jq '.nats_server.port  = "'${NATSPORT}'"' daemon.cfg | sponge daemon.cfg
jq '.nats_server.serverUUID  = "'${SERVERUUID}'"' daemon.cfg | sponge daemon.cfg
jq '.grpc_server.domain  = "'${SERVERDOMAIN}'"' daemon.cfg | sponge daemon.cfg
jq '.grpc_server.port  = "'${GRPCPORT}'"' daemon.cfg | sponge daemon.cfg
jq '.torrent.trackerDomain  = "'${SERVERDOMAIN}'"' daemon.cfg | sponge daemon.cfg
jq '.torrent.trackerPort  = "'${TRACKERPORT}'"' daemon.cfg | sponge daemon.cfg
jq '.torrent.localPort  = "'${DAEMONPORT}'"' daemon.cfg | sponge daemon.cfg
echo "nameserver 8.8.8.8" > /etc/resolv.conf
ps -ef | grep 'VerAI' | grep -v grep | awk '{print $2}' | xargs -r kill -9
rm -R /opt/VerAI/downloads/* 2&> /dev/null 
rm -R /opt/VerAI/projects/* 2&> /dev/null
rm -R /opt/VerAI/components/* 2&> /dev/null
rm -R /opt/VerAI/torrents/*  2&> /dev/null
rm -R /opt/VerAI/data/*  2&> /dev/null
rm -R /opt/VerAI/datasets/*  2&> /dev/null
rm -R /opt/VerAI/jnotebooks/*  2&> /dev/null
rm -R /opt/VerAI/torrents/.save_resume  2&> /dev/null
rm  /opt/VerAI/torrents.ini 2&> /dev/null
rm  /opt/VerAI/daemon.db 2&> /dev/null
rm  /opt/VerAI/daemon.log 2&> /dev/null
pip3 install --upgrade pip
pip3 install numpy grpcio grpcio-tools futures gitpython grpcio
pip3 install --upgrade grpcio
export LD_LIBRARY_PATH=/opt/VerAI/lib:${LD_LIBRARY_PATH}
cd /opt/VerAI
./bin/VerAIDaemon
