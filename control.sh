#!/bin/bash

APPNAME=lyanadmin # Name of the application
DJANGODIR=$(cd $(dirname $0)/; pwd) # Django project directory
USER=wangchao # the user to run as
NUM_WORKERS=4 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=$APPNAME.settings # which settings file should Django use
DJANGO_WSGI_MODULE=$APPNAME.wsgi # WSGI module name


cd $DJANGODIR
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
VARDIR=$DJANGODIR/var

test -d $VARDIR || mkdir -p $VARDIR

pidfile=var/$APPNAME.pid
logfile=var/$APPNAME.log
port=8000

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

    exec gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $APPNAME \
    --workers $NUM_WORKERS \
    --user=$USER \
    --bind=127.0.0.1:8000 \
    -D --pid $VARDIR/lyanadmin.pid \
    --capture-output  \
    --log-level=debug \
    --log-file=$VARDIR/lyanadmin.log & 2>&1
    sleep 1
    echo -n "$APPNAME started..., pid="
    cat $pidfile
}


function stop() {
    pid=`cat $pidfile`
    kill $pid
    echo "$APPNAME quit..."
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

