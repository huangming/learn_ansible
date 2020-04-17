#!/usr/bin/env bash

_curr_date=$(date +%Y%m%d)

basepath=$(cd `dirname $0`; pwd)

cd $basepath/..

export ANSIBLE_SSH_CONTROL_PATH_DIR=~/.ansible/backup

TEMP=`getopt -o th -a -l help,status:: -n "test.sh" -- "$@"`
# 判定 getopt 的执行时候有错，错误信息输出到 STDERR
if [ $? != 0 ]
then
	echo "Terminating....." >&2
	exit 1
fi

eval set -- "$TEMP"

while true
do
    case "$1" in
        -t | --status)
            /usr/local/bin/python3 scripts/status.py -abackup
            shift
            break
            ;;

        -h | --help)
            /usr/local/bin/python3 scripts/help.py -abackup
            shift
            break
            ;;

		--)
		    /usr/local/bin/python3 scripts/action.py -abackup
			shift
			break
			;;
		*)
			echo "Internal error!"
			exit 1
            ;;

    esac
done


