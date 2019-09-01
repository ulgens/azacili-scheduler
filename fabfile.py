#!/usr/bin/env python2
#
#  Requirements:
#     * Fabric==1.14.0
#     * fabtools==0.20.0
#
# Fabric doesn't support Python3. You should run tasks under py2 env.
#     ~ fab task_new -i key_file

# Troubleshooting:
#   Ssh key doesn't work:
#   * ssh-add -D  # Delete all identities from agent
#   * ssh-add keyname  # Add the key back to agent

from functools import partial
# noinspection PyUnresolvedReferences
from fabtools import require, python, files, git
# noinspection PyUnresolvedReferences
from fabric.api import sudo, env, run, cd, hosts, roles


env.roledefs = {
    'prod': ['developer@46.101.186.190'],
}

update_file = partial(require.file, use_sudo=True, verify_remote=True)


@roles('prod')
def app_deploy():
    # Pull repository
    run('eval `ssh-agent -s` && ssh-add')

    with cd("/home/developer/scheduler"):
        run("git fetch origin")
        run("git reset origin/master --hard")

    # Create / update config
    if files.is_file('/etc/nginx/sites-enabled/default'):
        files.remove('/etc/nginx/sites-enabled/default', use_sudo=True)

    update_file('/etc/systemd/system/gunicorn.service', source='conf/gunicorn.service')
    update_file('/etc/nginx/sites-available/www.azacili.com', source='conf/www.azacili.com')

    # Create / update Python environment
    with python.virtualenv("/home/developer/.pyenv/versions/azacili/"):
        with cd('/home/developer/scheduler'):
            run("pip install -r requirements/prod.txt --upgrade --upgrade-strategy eager")
            run(r"find . -name '*.pyc' -exec rm -rf {} \;")

            run("python manage.py collectstatic -c --noinput --settings=azacili.settings.prod")

    sudo("systemctl daemon-reload")
    sudo("service gunicorn restart")
    sudo("service nginx restart")

    return True
