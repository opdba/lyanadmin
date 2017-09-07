#!/bin/bash

WORKSPACE=$(cd $(dirname $0)/; pwd)
cd $WORKSPACE

mkdir -p var

app=lyanadmin
pidfile=var/$app.pid
logfile=var/$app.log
if [ X$2==X ]
then
port=8000
else
port=$2
fi

function check_pid() {
    if [ -f $pidfile ];then
        pid=`cat $pidfile`
        if [ -n $pid ]; then
            running=`ps -p $pid|grep -v "PID TTY" |wc -l`
            return $running
        fi
    fi
    return 0
}

function start() {
    check_pid
    running=$?
    if [ $running -gt 0 ];then
        echo -n "$app now is running already, pid="
        cat $pidfile
        return 1
    fi

    gunicorn -w 4 -b 127.0.0.1:$port lyanadmin.wsgi:application -D --pid $pidfile --capture-output --error-logfile var/error.log --log-level debug --log-file=$logfile &> $logfile 2>&1
    sleep 1
    echo -n "$app started..., pid="
    cat $pidfile
}

function stop() {
    pid=`cat $pidfile`
    kill $pid
    echo "$app quit..."
}

function kill9() {
    pid=`cat $pidfile`
    kill -9 $pid
    echo "$app stoped..."
}

function restart() {
    stop
    sleep 2
    start
}

function status() {
    check_pid
    running=$?
    if [ $running -gt 0 ];then
        echo -n "$app now is running, pid="
        cat $pidfile
    else
        echo "$app is stoped"
    fi
}

function tailf() {
    tail -f $logfile
}

function help() {
    echo "$0 start|stop|restart|status|tail|kill9|version|pack"
}

if [ "$1" == "" ]; then
    help
elif [ "$1" == "stop" ];then
    stop
elif [ "$1" == "kill9" ];then
    kill9
elif [ "$1" == "start" ];then
    start
elif [ "$1" == "restart" ];then
    restart
elif [ "$1" == "status" ];then
    status
elif [ "$1" == "tail" ];then
    tailf
elif [ "$1" == "pack" ];then
    pack
elif [ "$1" == "version" ];then
    show_version
else
    help
fi
