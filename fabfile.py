from fabric.api import *
from fabric.contrib import files
from fabric.operations import put
from fabric.context_managers import hide
import os
import fabfile_settings

global PROJECT_ID
global PROJECT_NAME
global PROJECT_PATH
global PROJECT_URL
global BRANCH
global REVERT_COMMIT
global DEPLOY_SCRIPT
global DEPLOY_SCRIPT_PATH
global DEPLOY_SCRIPT_LOCAL

env.warn_only = True
#env.skip_bad_hosts = True

DEPLOY_SCRIPT = 'deploy.sh'
DEPLOY_SCRIPT_LOCAL = os.path.join(os.path.dirname(__file__), DEPLOY_SCRIPT)
valid = True
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
        PROJECT_URL = settings['project_url']
        PROJECT_NAME = settings['project_name']
        BRANCH = settings['branch']
        DEPLOY_SCRIPT_PATH = os.path.join(PROJECT_PATH, DEPLOY_SCRIPT)
        env.user = settings['user']
        env.hosts = settings['hosts']
        env.key_filename = settings['ssh_key']
        print('Product: %s\n' % (PROJECT_NAME))
    else:
        print('Error secret key not valid')
        exit(1)
except AttributeError: 
    valid = False

def switch_back_4_version():
    """Switch back 4 versions on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -l 4' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')

def switch_back_3_version():
    """Switch back 3 versions on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -l 3' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')

def switch_back_2_version():
    """Switch back 2 versions on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -l 2' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')

def switch_back_1_version():
    """Switch back 1 version on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -l 1' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')

def switch_back_0_version():
    """Switch to latest version on product servers"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -l 0' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')

def deploy_info():
    """Get project deploy infomations"""
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -i' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')

@parallel
def revert_commit():
    """Revert project to a previous commit"""
    if not fabfile_settings.validate_setting(REVERT_COMMIT):
        print('Error revert commit key not valid')
        exit(1)
    if not files.exists(PROJECT_PATH):
        print('Error project not deployed yet')
        exit(1)
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s -r %s' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH, REVERT_COMMIT))
    print('\n')

@parallel
def deploy_product():
    """Clone the newest version of project and checkout"""
    if not files.exists(PROJECT_PATH):
        with hide('running'):
            run('mkdir -p %s' % (PROJECT_PATH))
    with hide('running'):
        put(DEPLOY_SCRIPT_LOCAL, DEPLOY_SCRIPT_PATH, mode=0755) 
        run('bash %s -p %s -u %s -b %s' % (DEPLOY_SCRIPT_PATH, PROJECT_PATH, PROJECT_URL, BRANCH))
    print('\n')
