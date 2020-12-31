for pid in $(ps -ef | awk '/runcron/ {print $2}'); do kill -9 $pid; done
