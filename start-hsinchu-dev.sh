export PYTHONIOENCODING=utf-8
/usr/bin/nohup /usr/local/bin/python3 /home/pms_plus/hsinchu_dev/main.py --env=hsinchu --port=8001> server.log 2>&1 &
echo "-----------current process--------------"
ps -ef|grep python3