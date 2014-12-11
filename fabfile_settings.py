# Fabfile settings
SSH_KEY_PATH = '/home/deploy/fabric-deploy/deploy-keys/'
INJECT = [ '\'', '\"', '#', '$', '(', ')', '*', '`', ',', ';', '&', '[', ']', '{', '}', '|' ]
PROJECT_SETTINGS = [
    {
        'id': '5HpOY4tZd2AKszmrSyKumxGK9Z7nfRjJireaKWkXucEz',
        'user': 'git',
        'branch': 'master',
        'hosts': ['web1.centos.local', 'web2.centos.local'],
        'ssh_key': SSH_KEY_PATH + 'git.key',
        'project_name': 'deploy-git',
        'project_path': '/var/www/test/deploy-git',
        'project_url': 'git@github.com:tongphe/fabric_git_deploy.git',
    },
    {
        'id': '5HpOY4tZd2AKszmrSyKumxGK9Z7nfRjJireaKWkXucEz',
        'user': 'git',
        'branch': 'master',
        'hosts': ['web1.centos.local', 'web2.centos.local'],
        'ssh_key': SSH_KEY_PATH + 'git.key',
        'project_name': 'deploy-git',
        'project_path': '/var/www/test/deploy-git',
        'project_url': 'git@github.com:tongphe/fabric_git_deploy.git',
    },
]

def validate_setting(setting):
    if not setting or any(char for char in INJECT if char in setting):
        return False
    else:
        return True

def get_settings(project_id):
    for set in PROJECT_SETTINGS:
        if set['id'] == project_id:
            return set
    return {}
