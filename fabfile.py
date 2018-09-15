from fabric.api import *
import cuisine
import urllib
import json

USERS = ['yuta1024', 'tyabuki', 'nhirokinet']
cuisine.select_package('yum')

@task
def init():
    _setup_user()
    _setup_kataribe()
    _setup_yum_repository()
    _setup_common_package()


@task
def install_nginx_and_php():
    sudo('yum install --enablerepo=epel,remi,remi-php72 nginx php php-mbstring php-pdo php-mysqlnd php-fpm php-gd -y')


@task
def install_mysql():
    sudo('yum install Percona-Server-server-57 percona-toolkit -y')


@task
def logrotate():
    if cuisine.file_exists('/var/log/nginx/access.log'):
        sudo('cp /var/log/nginx/access.log /var/log/nginx/access_`date +%s`.log')
        sudo('cp /dev/null /var/log/nginx/access.log')
    if cuisine.file_exists('/var/log/nginx/error.log'):
        sudo('cp /var/log/nginx/error.log /var/log/nginx/error_`date +%s`.log')
        sudo('cp /dev/null /var/log/nginx/error.log')
    if cuisine.file_exists('/var/log/mysql/slow-queries.log'):
        sudo('cp /var/log/mysql/slow-queries.log /var/log/mysql/slow-queries_`date +%s`.log')
        sudo('cp /dev/null /var/log/mysql/slow-queries.log')

    if cuisine.file_exists('/var/log/nginx/access.log'):
        sudo('systemctl restart nginx')
    if cuisine.file_exists('/var/log/mysql/slow-queries.log'):
        sudo('systemctl restart mysql')


def _setup_user():
    for user in USERS:
        keys = '\n'.join(_get_public_key_from_github(user))

        cuisine.user_ensure(user, shell='/bin/bash')
        cuisine.group_user_ensure('wheel', user)
        sudo('echo "password" | passwd --stdin %s' % user)

        sudo('mkdir -p /home/%s/.ssh' % user)
        sudo('chown %s:%s /home/%s/.ssh' % (user, user, user))
        sudo('chmod 700 /home/%s/.ssh' % user)

        sudo('echo "%s" > /home/%s/.ssh/authorized_keys' % (keys, user))
        sudo('chown %s:%s /home/%s/.ssh/authorized_keys' % (user, user, user))
        sudo('chmod 600 /home/%s/.ssh/authorized_keys' % user)


def _setup_kataribe():
    cuisine.package_ensure('unzip')

    temp_dir = run('mktemp -d')
    with cd(temp_dir):
        run('wget https://github.com/matsuu/kataribe/releases/download/v0.3.3/linux_amd64.zip')
        run('echo "9c4a4fe72651e33b1a6ef55f5e672fa38b755d48 linux_amd64.zip" | sha1sum -c -')
        run('unzip linux_amd64.zip kataribe')
        sudo('mv ./kataribe /usr/local/bin')
    run('rm -r %s' % temp_dir)


def _setup_yum_repository():
    cuisine.package_ensure('epel-release')
    if not cuisine.file_exists('/etc/yum.repos.d/remi.repo'):
        sudo('yum install https://rpms.remirepo.net/enterprise/remi-release-7.rpm -y')
    if not cuisine.file_exists('/etc/yum.repos.d/percona-release.repo'):
        sudo('yum install http://www.percona.com/downloads/percona-release/redhat/0.1-6/percona-release-0.1-6.noarch.rpm -y')
    if not cuisine.file_exists('/etc/yum.repos.d/nginx.repo'):
        nginx = ['[nginx]',
                 'name=nginx repo',
                 'baseurl=http://nginx.org/packages/centos/7/$basearch/',
                 'gpgcheck=0',
                 'enabled=1']
        sudo('echo \'%s\' > /etc/yum.repos.d/nginx.repo' % '\n'.join(nginx))


def _setup_common_package():
    cuisine.package_ensure('git')


def _get_public_key_from_github(user):
    url = 'https://api.github.com/users/%s/keys' % user
    res = json.loads(urllib.urlopen(url).read())

    keys = []
    for e in res:
        keys.append(e['key'])
    return keys
