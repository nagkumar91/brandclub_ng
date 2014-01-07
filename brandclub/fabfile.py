from fabric.colors import red, green
from fabric.context_managers import cd, shell_env
from fabric.operations import run, sudo, local
from fabric.state import env

env.hosts = ["beta.brandclub.mobi"]
env.user = 'brandclub'


def deploy():
    print(red("Pushing to server repo"))
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
