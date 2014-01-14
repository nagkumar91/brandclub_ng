from fabric.colors import red, green
from fabric.context_managers import cd, shell_env
from fabric.operations import run, sudo, local
from fabric.state import env

#env.hosts = ["beta.brandclub.mobi"]
#env.user = 'brandclub'

# To run use fab -H host_name -u user deploy

# Host is beta.brandclub.mobi user is brandclub
def deploy():
    print(red("Pushing to server repo"))
    local("git push origin develop")
    local("git push prod develop")
    with cd("/srv/www/brandclub"):
        sudo("git reset --hard || true", user="www-data")
        sudo("git pull", user="www-data")
        sudo("source /srv/bcenv/bin/activate && pip install -r requirements/production.txt > /dev/null", user="www-data")
    with cd("/srv/www/brandclub/brandclub"):
        with shell_env(DJANGO_SETTINGS_MODULE='brandclub.settings.production',
                       SECRET_KEY='bclub7fk21jj!=o&2nnv+f@(xhxsnn2tso+0o*ly7mdzzlr+zy3h&-2tib'):
            sudo("source /srv/bcenv/bin/activate && python manage.py collectstatic --noinput > /dev/null", user="www-data")
            sudo("source /srv/bcenv/bin/activate && ./manage.py migrate --no-initial-data", user="www-data")
        sudo("supervisorctl restart beta")
    print(green("Deployment complete"))


# To run use fab -H host_name -u user deploy_prod
#Host is srv1.brandclub.mobi user is bclub
def deploy_prod():
    print(red("Deploying to production server"))
    local('git push origin master')
    with cd("/opt/bclub/brandclub"):
        run("git reset --hard || true")
        run("git pull origin master")
        run("source /opt/bclub/.virtualenvs/bcenv/bin/activate && pip install -r requirements.txt")
    with cd("/opt/bclub/brandclub/brandclub"):
        with shell_env(DJANGO_SETTINGS_MODULE='brandclub.settings.prod',
                       SECRET_KEY='bclubmfw0w!ipbgtlen=&m^3i(f$by2oi$$7!7$xrqioag3*^pane+0prod'):
            run("source /opt/bclub/.virtualenvs/bcenv/bin/activate && python manage.py collectstatic --noinput > /dev/null")
            run("source /opt/bclub/.virtualenvs/bcenv/bin/activate && ./manage.py migrate --no-initial-data")
        sudo("supervisorctl restart brandclub")
    print(green("Deployment complete"))

