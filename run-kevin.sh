#!/bin/sh
PORT=8003
FOLDER="pms_plus_kevin"
if [ "$1" == "pad-demo" ] 
then
    sudo /usr/bin/nohup /usr/local/bin/python3 /home/ec2-user/servers/pmsplus-server-pad-demo/main.py --env=pad-demo --port=8001> server-demo.log 2>&1 &
elif [ "$1" == "pad-poc" ] 
then
    sudo /usr/bin/nohup /usr/local/bin/python3 /home/ec2-user/servers/pad-poc/main.py --env=pad-poc --port=8901> server.log 2>&1 &
elif [ "$1" == "qa" ] 
then
    sudo /usr/bin/nohup /usr/local/bin/python3 /home/ec2-user/servers/qa/main.py --env=qa --port=8902> server.log 2>&1 &
elif [ "$1" == "pad-devel" ] 
then
    PORT=8000
    FOLDER="pmsplus-server-pad-devel"

elif [ "$1" == "test" ] 
then
    sudo /usr/bin/nohup /usr/local/bin/python3 /home/ec2-user/servers/pmsplus-server-test/main.py --env=pad-devel --port=8000> server.log 2>&1 &
elif [ "$1" == "doc" ] 
then
    PORT=8902
    FOLDER="doc"
elif [ "$1" == "kevin" ]
then
    PORT=8003
    FOLDER="pmsplus-server"
elif [ "$1" == "prod" ]
then
    PORT=8901
    FOLDER="prod"
elif [ "$1" == "fee" ]
then
    PORT=8904
    FOLDER="pmsplus_server_fee"
fi
    /usr/bin/nohup /usr/local/bin/python3 /home/pms_plus/$FOLDER/main.py --env=$FOLDER --port=$PORT> server.log 2>&1 &
if [ "$2" == "k" ]
then
   echo "kill server $1"
else
   echo "running server $1"
fi

if [ "$2" == "k" ]
then
        ps -ef | grep "$PORT"
	PID=`ps -ef | grep "$PORT" |grep -v grep | awk '{print$2}' | awk 'FNR == 1'`
	echo killing PID = "$PID"
        if [ -n "$PID" ]; then
		kill `ps -ef | grep "$PORT" |grep -v grep | awk '{print$2}' | awk 'FNR == 1'`
        	echo " -----checking server current process -----"
        	sleep 2
        	ps -ef | grep $PORT
	else
		echo "server is not running"
	fi
else
    echo "/usr/bin/nohup /usr/local/bin/python3 /home/ec2-user/servers/$FOLDER/main.py --env=$FOLDER --port=$PORT> server.log 2>&1 & fi"

fi

