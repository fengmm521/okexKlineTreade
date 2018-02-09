#!bin/bash

export PATH=/usr/bin/:/usr/local/bin:/bin:


DATE=`date "+%Y-%m-%d %H:%M:%S"`
echo $DATE

svn up

LOG=`nohup python klinetool1hour.py > logtest.txt 2>&1 & echo $!`
# LOG="12345"
echo $LOG
OUTSTR=$DATE"\n"$LOG
echo $OUTSTR > psidtest.txt
echo '程序已启动'