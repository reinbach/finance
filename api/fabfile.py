from __future__ import with_statement
from fabric.api import *  # noqa

env.app = 'api_finance'
env.hosts = ['web1']
env.sites_dir = '/opt/sites/'
env.app_dir = env.sites_dir + env.app
env.repo = "https://github.com/reinbach/api_finance"
env.nginx_conf_dir = "/opt/nginx/conf/sites/"

USE_DB = True


def init_db():
    if USE_DB:
        run("source {app_dir}/bin/activate && python manage.py syncdb".format(
            app_dir=env.app_dir))
        run("source {app_dir}/bin/activate && python manage.py migrate".format(
            app_dir=env.app_dir))
    run("""source {d}/bin/activate &&
        python manage.py collectstatic -v0 --noinput""".format(d=env.app_dir))


def build_app():
    run("source {app_dir}/bin/activate && python setup.py install".format(
        app_dir=env.app_dir))
    run("cp {app_dir}/master/nginx.conf {nginx_conf_dir}{app}.conf".format(
        app_dir=env.app_dir,
        nginx_conf_dir=env.nginx_conf_dir,
        app=env.app))


def install():
    """Installs app on server"""
    with settings(user="root"):
        run("virtualenv --no-site-packages -p python2 {app_dir}".format(
            app_dir=env.app_dir))
        with cd(env.app_dir):
            # clone repo
            run("git clone {repo} master".format(repo=env.repo))
            with cd("master"):
                build_app()
                with cd("{app}".format(app=env.app)):
                    with cd("settings"):
                        run("rm -f currentenv.py")
                        run("ln -s prod.py currentenv.py")
                    init_db()
        run("/etc/rc.d/uwsgi reload")
        run("/etc/rc.d/nginx reload")


def update():
    """Updates code base on server"""
    with settings(user="root"):
        with cd("{app_dir}/master".format(app_dir=env.app_dir)):
            run("git pull")
            build_app()
            with cd("{app}".format(app=env.app)):
                init_db()
        run("/etc/rc.d/uwsgi reload")
        run("/etc/rc.d/nginx reload")
