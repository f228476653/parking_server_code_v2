#!/usr/bin/sh

STOP=0
RUN=1
while [ $RUN ]; do
    timestamp=$(date +%T)
    echo `date`
    echo "Time : $timestamp"
    echo "STOP is now $STOP"
    if [ $STOP -lt 20000000000000 ]; then
        echo "STOP is $STOP"
        /home/pms_plus/pmsplus-server/./cron_einvoice.sh >> /home/pms_plus/pmsplus-server/cron.log 2>&1 &
        /home/pms_plus/pmsplus-server/./cron_lane.sh >> /home/pms_plus/pmsplus-server/cron.log 2>&1 &
        /home/pms_plus/pmsplus-server/./cron_parking.sh >> /home/pms_plus/pmsplus-server/cron.log 2>&1 &
        /home/pms_plus/pmsplus-server/./cron_trxdata.sh >> /home/pms_plus/pmsplus-server/cron.log 2>&1 &
        /home/pms_plus/pmsplus-server/./cron_real-time.sh >> /home/pms_plus/pmsplus-server/cron.log 2>&1 &
        echo "sleeping 4 min"
        sleep 4m
        echo "after sleep"
        ((STOP++))
    else
        ((RUN--))
    fi
done

