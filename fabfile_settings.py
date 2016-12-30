# Fabfile settings
import time
import uuid
import smtplib
from email.mime.text import MIMEText
import os

SSH_KEY_PATH = '/home/fabric/deploy-keys/'
INJECT = [ '\'', '\"', '#', '$', '(', ')', '*', '`', ',', ';', '&', '[', ']', '{', '}', '|', '<' , '>' ]

DEPLOY_NOTIFY = {
    'from': 'fabric-deploy@fabric.com',
    'to': ['sysadmin@fabric.com'],
    'server': 'mail.fabric.com',
    'port': 587,
    'username': 'notification',
    'password': 'MhxOIROxVu9UBBrmI',
}

DEPLOY_SETTINGS = [
    {
        'id': 'MyimOXc3tCpy2dZ7MOVtECxscOIrQG8EzT2Ffn71jcgz',
        'user': 'fabric',
        'branch': 'master',
        'hosts': ['172.16.2.1', '172.16.2.2', '172.16.2.3'],
        'ssh_key': SSH_KEY_PATH + 'fabric.key',
        'project_name': 'api.fabric.com',
        'project_path': '/data/webroot/api.fabric.com',
        'project_url': 'git@github.com:tongphe/fabric-git-deploy.git',
        'command': [
            '/usr/local/bin/composer dump-auto',
        ],
        'notify_sysadmin': True,
        'notify_dev': True,
        'notify_devaddrs': ['dev.fabric.com'],
    },
]


def validate_setting(setting):
    if not setting or any(char for char in INJECT if char in setting):
        return False
    else:
        return True


def get_settings(project_id):
    for set in DEPLOY_SETTINGS:
        if set['id'] == project_id:
            set['uuid'] = str(uuid.uuid1())
            return set
    return {}


def deploy_init_confirm(hosts_file):
    try:
        with open(hosts_file, 'a'):
            os.utime(hosts_file, None)
    except Exception, e:
        pass


def deploy_finish_confirm(hosts_file):
    try:
        os.remove(hosts_file)
    except OSError:
        pass


def deploy_ready_confirm(host, hosts_file):
    if not os.path.isfile(hosts_file):
        return False
    h_file = open(hosts_file, 'a')
    h_file.write(host + '\n')
    h_file.close()
    return True


def wait_all_host_ready(hosts_list, hosts_file, second_timeout):
    expire = 0
    while expire < second_timeout:
        expire += 1
        if not os.path.isfile(hosts_file):
            return False
        if check_all_host_ready(hosts_list, hosts_file):
            return True
        time.sleep(1)
    return False


def check_all_host_ready(hosts_list, hosts_file):
    try:
        h_file = open(hosts_file, 'r')
    except IOError:
        return False
    hosts_ready = []
    for host in h_file.readlines():
        hosts_ready.append(host.rstrip('\n'))

    return set(hosts_ready) == set(hosts_list)


def notify_deployment(subject, body, sysadmin=False, devaddrs=[]):
    send_to = []
    if not sysadmin and not devaddrs:
        return False
    if sysadmin:
        send_to += DEPLOY_NOTIFY['to']
    if devaddrs:
        send_to += devaddrs

    message = MIMEText(body)
    message['From'] = DEPLOY_NOTIFY['from']
    if sysadmin and not devaddrs:
        message['To'] = ', '.join(DEPLOY_NOTIFY['to'])
    if not sysadmin and devaddrs:
        message['To'] = ', '.join(devaddrs)
    if sysadmin and devaddrs:
        message['To'] = ', '.join(DEPLOY_NOTIFY['to'])
        message['Cc'] = ', '.join(devaddrs)
    message['Subject'] = subject

    try:
        server = smtplib.SMTP(host=DEPLOY_NOTIFY['server'], port=DEPLOY_NOTIFY['port'], timeout=3)
        server.starttls()
        server.login(DEPLOY_NOTIFY['username'], DEPLOY_NOTIFY['password'])
        server.sendmail(DEPLOY_NOTIFY['from'], send_to, message.as_string())
        server.quit()
    except Exception, e:
        return False
    return True
