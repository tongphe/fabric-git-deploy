from fabric.api import *
from fabric.contrib import files
from fabric.operations import put
from fabric.context_managers import hide
import os
import fabfile_settings
import time
from datetime import datetime

global PROJECT_ID
global PROJECT_PATH
global PROJECT_NAME
global PROJECT_URL
global BRANCH
global REVERT_COMMIT
global COMMAND
global DEPLOY_SCRIPT
global DEPLOY_SCRIPT_PATH
global DEPLOY_SCRIPT_LOCAL
global ORIGIN_PATH
global HOSTS_FILE
global WAIT_DEPLOY_TIMEOUT
global DEPLOY_DATETIME
global NOTIFY_SYSADMIN
global NOTIFY_DEV
global NOTIFY_DEV_ADDRS
global LOCK_FILE_PATH
global DEPLOY_START_TIME
global DEPLOY_END_TIME

valid = True
DEPLOY_DATETIME = time.strftime("%Y-%m-%d %H:%M")
DEPLOY_START_TIME = datetime.now()
WAIT_DEPLOY_TIMEOUT = 300
DEPLOY_SCRIPT = 'deploy.sh'
LOCK_FILE = 'deploy.lock'
DEPLOY_SCRIPT_LOCAL = os.path.join(os.path.dirname(__file__), DEPLOY_SCRIPT)
HOSTS_FILE_DIR = '/var/run/deploy'
if not os.access(HOSTS_FILE_DIR, os.W_OK) or not os.access(HOSTS_FILE_DIR, os.R_OK):
    print('Error deloy control file not touchable')
    exit(1)
# Validate user data
try:
    REVERT_COMMIT = env.revert_commit
except AttributeError: 
    REVERT_COMMIT = ''

try:
    PROJECT_ID = env.secret
    if not fabfile_settings.validate_setting(PROJECT_ID):
        valid = False
    else:
        settings = fabfile_settings.get_settings(PROJECT_ID)
        if not settings:
            valid = False
    if valid:
        PROJECT_PATH = settings['project_path']
        ORIGIN_PATH = os.path.join(PROJECT_PATH, 'origin')
        PROJECT_URL = settings['project_url']
        PROJECT_NAME = settings['project_name']
        BRANCH = settings['branch']
        DEPLOY_SCRIPT_PATH = os.path.join(PROJECT_PATH, DEPLOY_SCRIPT)
        LOCK_FILE_PATH = os.path.join(PROJECT_PATH, LOCK_FILE)
        HOSTS_FILE = os.path.join(HOSTS_FILE_DIR, settings['uuid'])
        fabfile_settings.deploy_init_confirm(HOSTS_FILE)
        env.user = settings['user']
        env.hosts = settings['hosts']
        env.key_filename = settings['ssh_key']
        # Optional settings
        try:
            COMMAND = settings['command']
        except KeyError:
            COMMAND = ''
        try:
            NOTIFY_SYSADMIN = settings['notify_sysadmin']
        except KeyError:
            NOTIFY_SYSADMIN = False
        try:
            NOTIFY_DEV = settings['notify_dev']
        except KeyError:
            NOTIFY_DEV = False
        try:
            NOTIFY_DEV_ADDRS = settings['notify_devaddrs']
        except KeyError:
            NOTIFY_DEV_ADDRS = []
        if not NOTIFY_DEV:
            NOTIFY_DEV_ADDRS = []
        print('Product %s:' % (PROJECT_NAME))
    else:
        print('Error secret key not valid')
        exit(1)
except AttributeError: 
    valid = False


@parallel
def switch_back_4_version():
    """Switch back 4 versions on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -l 4' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        print('[%s]:' % (env.host_string))
        print res
        print('=======================================================================')


@parallel
def switch_back_3_version():
    """Switch back 3 versions on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -l 3' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        print('[%s]:' % (env.host_string))
        print res
        print('=======================================================================')


@parallel
def switch_back_2_version():
    """Switch back 2 versions on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -l 2' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        print('[%s]:' % (env.host_string))
        print res
        print('=======================================================================')


@parallel
def switch_back_1_version():
    """Switch back 1 version on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -l 1' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        print('[%s]:' % (env.host_string))
        print res
        print('=======================================================================')


@parallel
def switch_back_0_version():
    """Switch to latest version on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -l 0' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        print('[%s]:' % (env.host_string))
        print res
        print('=======================================================================')


@parallel
def deploy_info():
    """Get project deploy infomations"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -i' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        print('[%s]:' % (env.host_string))
        print res
        print('=======================================================================')


@parallel
def revert_commit():
    """Revert project to a previous commit"""
    return_code = 0
    if not fabfile_settings.validate_setting(REVERT_COMMIT):
        print('Error revert commit key not valid')
        exit(1)
    if not files.exists(PROJECT_PATH):
        with hide('running'):
            run('mkdir -p %s' % (PROJECT_PATH))
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s -r %s' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH, REVERT_COMMIT))
        print ''
        if 'Error' in res:
            print('[%s]: Failed' % (env.host_string))
            print res
            print 'Deploy cancelled.'
            return_code = 1
        elif fabfile_settings.deploy_ready_confirm(env.host_string, HOSTS_FILE) and fabfile_settings.wait_all_host_ready(env.hosts, HOSTS_FILE, WAIT_DEPLOY_TIMEOUT):
            print('[%s]: Success' % (env.host_string))
            print res
            print ''
            for cmd in COMMAND:
                with cd(ORIGIN_PATH):
                    print('Run: %s' % (cmd))
                    output = run('%s' % (cmd))
                    if output:
                        print output
            res_c = run('bash %s -p %s -u %s -b %s -c' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
            print res_c
            DEPLOY_END_TIME = datetime.now()
            deploy_total_time = (DEPLOY_END_TIME - DEPLOY_START_TIME).seconds
            if deploy_total_time < 5:
                time.sleep(5)
            else:
                time.sleep(3)
            if env.host_string == env.hosts[0]:
                msg_subject = 'Deploying product ' + PROJECT_NAME
                msg_body = '[' + DEPLOY_DATETIME + ']: Successfully deployed ' + PROJECT_NAME + ' on ' + str(len(env.hosts)) + ' servers ' + str(env.hosts) + ' in ' + str(deploy_total_time) + 's' + '\n\n' + 'Deloyment log:' + '\n' + res_c
                fabfile_settings.notify_deployment(subject=msg_subject, body=msg_body, sysadmin=NOTIFY_SYSADMIN, devaddrs=NOTIFY_DEV_ADDRS)
            print 'Total time: ' + str(deploy_total_time) + 's'
        else:
            if files.exists(LOCK_FILE_PATH):
                with hide('running', 'stdout'):
                    run('rm %s' % (LOCK_FILE_PATH))
            print('[%s]: Failed' % (env.host_string))
            print 'Deploy cancelled.'
            return_code = 1
        fabfile_settings.deploy_finish_confirm(HOSTS_FILE)
        print('=======================================================================')
        exit(return_code)


@parallel
def deploy_product():
    """Clone the newest version of project and checkout"""
    return_code = 0
    if not files.exists(PROJECT_PATH):
        with hide('running'):
            run('mkdir -p %s' % (PROJECT_PATH))
    with hide('running', 'stdout'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        res = run('bash %s -p %s -u %s -b %s' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
        print ''
        if 'Error' in res:
            print('[%s]: Failed' % (env.host_string))
            print res
            print 'Deploy cancelled.'
            return_code = 1
        elif fabfile_settings.deploy_ready_confirm(env.host_string, HOSTS_FILE) and fabfile_settings.wait_all_host_ready(env.hosts, HOSTS_FILE, WAIT_DEPLOY_TIMEOUT):
            print('[%s]: Success' % (env.host_string))
            print res
            print ''
            for cmd in COMMAND:
                with cd(ORIGIN_PATH):
                    print('Run: %s' % (cmd))
                    output = run('%s' % (cmd))
                    if output:
                        print output
            res_c = run('bash %s -p %s -u %s -b %s -c' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
            print res_c
            DEPLOY_END_TIME = datetime.now()
            deploy_total_time = (DEPLOY_END_TIME - DEPLOY_START_TIME).seconds
            if deploy_total_time < 5:
                time.sleep(5)
            else:
                time.sleep(3)
            if env.host_string == env.hosts[0]:
                msg_subject = 'Deploying product ' + PROJECT_NAME
                msg_body = '[' + DEPLOY_DATETIME + ']: Successfully deployed ' + PROJECT_NAME + ' on ' + str(len(env.hosts)) + ' servers ' + str(env.hosts) + ' in ' + str(deploy_total_time) + 's' + '\n\n' + 'Deloyment log:' + '\n' + res_c
                fabfile_settings.notify_deployment(subject=msg_subject, body=msg_body, sysadmin=NOTIFY_SYSADMIN, devaddrs=NOTIFY_DEV_ADDRS)
            print 'Total time: ' + str(deploy_total_time) + 's'
        else:
            if files.exists(LOCK_FILE_PATH):
                with hide('running', 'stdout'):
                    run('rm %s' % (LOCK_FILE_PATH))
            print('[%s]: Failed' % (env.host_string))
            print 'Deploy cancelled.'
            return_code = 1
        fabfile_settings.deploy_finish_confirm(HOSTS_FILE)
        print('=======================================================================')
        exit(return_code)
