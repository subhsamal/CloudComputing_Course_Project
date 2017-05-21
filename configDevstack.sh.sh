#!/bin/sh
###Author: Ankur###

#Set password and install softwares required
set pass "123456"
sudo apt-get install vim git ssh
send $pass

#Clone devstack
git clone https://git.openstack.org/openstack-dev/devstack

#Create and write to devstack/local.conf

touch devstack/local.conf

#Fetch and store value of ip address and interface
iface=$(ip -o link show | awk -F': ' '{print $2}' | tail -1)
ipaddr=$(ip addr show $iface | grep "inet\b" | awk '{print $2}' | cut -d/ -f1)


cat << EOM > devstack/local.conf
[[local|localrc]]
HOST_IP=$ipaddr
HOST_IP_IFACE=$iface
FLAT_INTERFACE=virbr0
PUBLIC_INTERFACE=$iface
SERVICE_HOST=$ipaddr
MYSQL_HOST=$ipaddr
RABBIT_HOST=$ipaddr
GLANCE_HOSTPORT=$ipaddr:9292
ADMIN_PASSWORD=123456
DATABASE_PASSWORD=123456
RABBIT_PASSWORD=123456
SERVICE_PASSWORD=123456

### Disable Nova-Services ###
disable_service n-net

### Enable Neutron ###
ENABLED_SERVICES+=,q-svc,q-dhcp,q-meta,q-agt,q-l3

###Neutron Options##
Q_USE_SECGROUP=True
FLOATING_RANGE="192.168.1.0/24"
FIXED_RANGE="10.0.0.0/24"
Q_FLOATING_ALLOCATION_POOL=start=192.168.1.2,end=192.168.1.254
PUBLIC_NETWORK_GATEWAY="192.168.1.1"
PUBLIC_INTERFACE=eth0
EOM

##Provide password less priviliges to stack user
sudo devstack/tools/create-stack-user.sh

##Create ssh-key 
mkdir ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t rsa
