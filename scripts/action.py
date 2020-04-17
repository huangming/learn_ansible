#!/usr/local/bin/python3
# -*- coding: utf-8 -*-


import os
from optparse import OptionParser
import subprocess
import yaml
# from status import StatusJson
import time

curr_path = os.path.abspath(os.path.dirname(__file__))
deploy_path = os.path.abspath(os.path.join(curr_path, '..'))
conffile = os.path.abspath(os.path.join(curr_path, '../automatic.yml'))


def run_main():
    # 解析命令行参数
    usage = 'usage: %prog [options] arg '
    parser = OptionParser(usage=usage, version='%prog 1.0.0.0')

    parser.add_option(
        "-t",
        "--task",
        type='string',
        default='',
        metavar="operation_task",
        help="待执行的命令(例:dep; start; stop; backup)")

    parser.add_option(
        "-b",
        "--bookfile",
        type='string',
        default='',
        metavar="playbook_file",
        help="待执行的playbook路径")

    parser.add_option(
        "-p",
        "--patterns",
        type='string',
        default='none',
        metavar="inventory patterns",
        help="patterns for items in inventory")

    parser.add_option(
        "-m",
        "--commands",
        type='string',
        default='',
        metavar="Ad-Hoc Commands",
        help="Ad-Hoc Commands")

    parser.add_option(
        "-a",
        "--args",
        type='string',
        default='',
        metavar="ansible command args",
        help="args use for ansible command,only work with -m arg")

    (options, _) = parser.parse_args()

    try:
        conf = yaml.load(open(conffile, 'r'))
    except Exception as e:
        print(e)
        return

    swf_operation_action = ''
    playbooks_file = ''
    # swf_trd_date_dir = './'
    swf_system_taget = conf.get('taget')
    swf_system_broker = conf.get('broker')
    swf_system_name = conf.get('system')
    version = conf.get('version')
    swf_system_version = swf_system_name + "-" + version

    if options.task != '':
        swf_operation_action = options.task.strip()
    elif options.bookfile != '':
        playbooks_file = options.bookfile.strip()
    elif options.commands != '':
        commands = options.commands.strip()
        args = options.args.strip()

    # 必须指定参数
    patterns = options.patterns.strip()
    inventory_file = ' inventory/swf_' + swf_system_name + '/' + swf_system_broker + '_hosts_' + swf_system_taget + ' '

    # 控制类任务
    if swf_operation_action == 'dep':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_dep.yml '

    elif swf_operation_action == 'stop':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_stop.yml '
    elif swf_operation_action == 'stop_register':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_stop_register.yml '
    elif swf_operation_action == 'backup':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_backup.yml '
    elif swf_operation_action == 'backup_register':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_backup_register.yml '
    elif swf_operation_action == 'backup_no_register':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_backup_no_register.yml '
    elif swf_operation_action == 'ntp':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_ntp.yml '
    elif swf_operation_action == 'open':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_open.yml '
    elif swf_operation_action == 'close':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/control/' + swf_system_name + '_close.yml '

    # 安装类任务
    elif swf_operation_action == 'install':
        playbooks_file = ' swf_playbooks/os/common/' + 'os_install_software.yml '
    elif swf_operation_action == 'software_check':
        playbooks_file = ' swf_playbooks/os/common/' + 'os_software_check.yml '
    elif swf_operation_action == 'ssh_key':
        playbooks_file = ' swf_playbooks/os/common/' + 'os_ssh_key.yml '

    # 测试类任务
    elif swf_operation_action == 'ping':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/test/' + swf_system_name + '_ping.yml '
    elif swf_operation_action == 'check_dir':
        playbooks_file = ' swf_playbooks/swf_' + swf_system_name + '/directory_checker.yml '

    else:
        if options.bookfile != '':
            playbooks_file = options.bookfile.strip()
        elif options.commands != '':
            commands = options.commands.strip()
            patterns = options.patterns.strip()
            args = options.args.strip()
        else:
            print(u'未知任务类型 {}'.format(swf_operation_action))
            return

    curr_date = time.strftime("%Y%m%d", time.localtime())
    os.putenv('ANSIBLE_LOG_PATH', 'logs/ansible-{}-{}.log'.format(swf_operation_action, curr_date))
    # 可选参数指定
    if playbooks_file != '':
        patterns = '' if patterns == 'all' else ' --limit %s '%patterns
        cmd = '$(which ansible-playbook) -i ' \
                        + inventory_file      \
                        + playbooks_file      \
                        + patterns      \
                        + " --extra-vars 'ansible_path_ansible_home={}'".format( deploy_path)
    else:
        args = ' -a %s'%args if args != '' else ''
        cmd = 'ansible -i ' + inventory_file + patterns + ' -m ' + commands + args 
    print("执行的命令为:  {}".format(cmd))
    ret_code = subprocess.call(cmd, shell=True, cwd=os.getcwd())

    # status_json = StatusJson()

    # status_json.record_action(swf_operation_action, playbooks_file)

    return ret_code


if __name__ == '__main__':
    print(u'exec over: {}'.format(0 == run_main() and 'success' or 'failed'))

