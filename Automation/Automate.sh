#!/bin/bash
####AUTHOR : Ashwin

##Network name and subnet name
networkName="privateNetwork"
subnetName="privateNetwork_sub"

##router name
routerName="router"
##range of IP
range="10.0.0.0/24"

## Import Key for SSH
KEY="Key"

##Specify the boot Image
BOOTIMG="cirros-0.3.4-x86_64-uec"

##Specify the flavor
FLAVOR="m1.tiny"

##Specify the name of Vm's
NAMEVM1='VM1'
NAMEVM2='VM2'

##Tap service and flow names
TapService='TS'
TapFlow='TF'



##source the session 
source ~/devstack/openrc admin admin


##create network
echo "creating network "${networkName}""

var=$(neutron net-create "${networkName}")

## Create router
echo "creating router"
neutron router-create "$routerName"

##Create subnet
echo "creating subnet"
neutron subnet-create "$networkName" "$range" --name "$subnetName"



##external interface ID
extInterface=$(neutron net-list | \
		grep public |	   \
		awk '{print $2}')

##Internal Interface ID
intInterface=$(neutron subnet-list |   \
		grep "$subnetName" | \
		awk '{print $2}')

##Router ID
routerID=$(neutron router-list | \
		grep "$routerName" | \
		awk  '{print $2}')

##Attach gateway to router
echo "creating router gateway"
neutron router-gateway-set "$routerName" "$extInterface"

##Attach interface private to router
echo "creating interface add"
neutron router-interface-add "$routerName" "$intInterface"

## Create port for Tap service 
echo "creating tap service port"
portIDService=$(neutron port-create "$networkName" | grep -w id | awk '{print $4}')

## Create port for Tap flow
echo "creating tap flow port"
portIdflow=$(neutron port-create "$networkName" | grep -w id | awk '{print $4}')

## Create tap service
echo "creating tap service"
neutron tap-service-create --name "$TapService" --port "$portIDService" 

## Create Tap flow
echo "creating tap flow"
neutron tap-flow-create --name "$TapFlow" --port "$portIdflow" --tap-service "$TapService" \
--direction "BOTH"


echo $portIDService
echo $portIdflow


## Boot Vms now
echo "creating boot vms"
VMUUID=$(nova boot \
	--nic port-id="$portIDService"\
        --image "${BOOTIMG}" \
        --flavor "${FLAVOR}" \
        --key-name "${KEY}" $NAMEVM1);

VMUUID1=$(nova boot \
	--nic port-id="$portIdflow" \
        --image "${BOOTIMG}" \
        --flavor "${FLAVOR}" \
        --key-name "${KEY}" $NAMEVM2);











		








	
