#!/bin/bash

function die()
{
	echo "Telnet failed, are you on the ardrone network?";
	exit 1;
}

echo "/data/wifi.sh" | telnet 192.168.1.1;
echo $?;
while ! ping -c 1 -W 1 192.168.1.207 >/dev/null 2>&1;
do
	echo "Waiting for drone... (now you need to connect to wasp_7)"
done;
echo "Parrot is alive!"
