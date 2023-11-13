'''make.py: Logic used by the project Makefile.

Usage:
    make.py <project> <action>
'''

import json
import os
import os.path
import subprocess
import sys

from docopt import docopt

###############################################################################

WORKING_PATH = os.path.abspath(os.getcwd())
SCRIPT_PATH = os.path.abspath(__file__)
APP_PATH = os.path.join(WORKING_PATH, 'app')

DOCKER_WORKING_PATH             = '/usr/src/app'
DOCKER_TEST_CLIENT_DOCKERFILE   = 'Makefile.d/dockerfiles/test-client.Dockerfile'
DOCKER_TEST_CLIENT_IMAGE        = 'django-test-client:{tag}'
DOCKER_TEST_CLIENT_NAME         = 'django_test_client_{tag}'
DOCKER_TEST_NETWOK_NAME         = 'django_test_network_{tag}'
DOCKER_TEST_SERVER_DOCKERFILE   = 'Makefile.d/dockerfiles/test-server.Dockerfile'
DOCKER_TEST_SERVER_IMAGE        = 'django-test-server:{tag}'
DOCKER_TEST_SERVER_NAME         = 'django_test_server_{tag}'

###############################################################################


def docker_testclient_image_exists(project_name):
    command = 'docker images {filter}|grep -qw "{tag}"'.format(
        filter=DOCKER_TEST_CLIENT_IMAGE.format(tag=project_name),
        tag=project_name,
    )
    return os.system(command) == 0


def docker_testclient_image_build(project_name):
    command = 'docker build -t {tag} -f {dockerfile} {context}'.format(
        tag=DOCKER_TEST_CLIENT_IMAGE.format(tag=project_name),
        dockerfile=DOCKER_TEST_CLIENT_DOCKERFILE,
        context=WORKING_PATH,
    )
    return os.system(command)


def docker_testclient_image_clean(project_name):
    if not docker_testclient_image_exists(project_name):
        return 0
    command = 'docker image rm {tag}'.format(
        tag=DOCKER_TEST_CLIENT_IMAGE.format(tag=project_name),
    )
    return os.system(command)


def docker_testclient_run(project_name, server_host, server_port, exec=None):
    if not docker_testclient_image_exists(project_name):
        print('Test client image does not exist, building...')
        docker_testclient_image_build(project_name)
    command = 'docker run -it --rm {name} {network} {volume} {env} {tag} {command}'.format(
        command=exec if exec else 'make help',
        env='-e SERVER_HOST={host} -e SERVER_PORT={port}'.format(
            host=server_host,
            port=server_port,
        ),
        name='--name {}'.format(DOCKER_TEST_CLIENT_NAME.format(tag=project_name)),
        network='--network {}'.format(DOCKER_TEST_NETWOK_NAME.format(tag=project_name)),
        tag=DOCKER_TEST_CLIENT_IMAGE.format(tag=project_name),
        volume='-v {project_path}:{docker_path}'.format(
            project_path=WORKING_PATH,
            docker_path=DOCKER_WORKING_PATH,
        ),
    )
    print(command)
    return os.system(command)


###############################################################################


def docker_testserver_address(project_name):
    command = 'docker container inspect {name}'.format(
        name=DOCKER_TEST_SERVER_NAME.format(tag=project_name),
    )
    data = json.loads(subprocess.check_output(command, shell=True).decode('utf-8').strip())
    return data[0]['NetworkSettings']['Networks'][DOCKER_TEST_NETWOK_NAME.format(tag=project_name)]['IPAddress']


def docker_testserver_image_exists(project_name):
    command = 'docker images {filter}|grep -qw "{tag}"'.format(
        filter=DOCKER_TEST_SERVER_IMAGE.format(tag=project_name),
        tag=project_name,
    )
    return os.system(command) == 0


def docker_testserver_image_build(project_name):
    command = 'docker build -t {tag} -f {dockerfile} {context}'.format(
        tag=DOCKER_TEST_SERVER_IMAGE.format(tag=project_name),
        dockerfile=DOCKER_TEST_SERVER_DOCKERFILE,
        context=APP_PATH,
    )
    return os.system(command)


def docker_testserver_image_clean(project_name):
    if not docker_testserver_image_exists(project_name):
        return 0
    command = 'docker image rm {tag}'.format(
        tag=DOCKER_TEST_SERVER_IMAGE.format(tag=project_name),
    )
    return os.system(command)


def docker_testserver_run(project_name, exec=None):
    if not docker_testserver_image_exists(project_name):
        print('Test server image does not exist, building...')
        docker_testserver_image_build(project_name)
    command = 'docker run -it --rm {name} -p 8000:8000 {volume} {tag} {command}'.format(
        command=exec if exec else 'python manage.py runserver 0.0.0.0:8000',
        name='--name {}'.format(DOCKER_TEST_SERVER_NAME.format(tag=project_name)),
        tag=DOCKER_TEST_SERVER_IMAGE.format(tag=project_name),
        volume='-v {app_path}:{docker_path}'.format(
            app_path=APP_PATH,
            docker_path=DOCKER_WORKING_PATH,
        ),
    )
    return os.system(command)


def docker_testserver_run_daemon(project_name, exec=None):
    if not docker_testserver_image_exists(project_name):
        print('Test server image does not exist, building...')
        docker_testserver_image_build(project_name)
    command = 'docker run --rm -d {name} {volume} {network} {tag} {command}>/dev/null'.format(
        command=exec if exec else 'python manage.py runserver 0.0.0.0:8000',
        name='--name {}'.format(DOCKER_TEST_SERVER_NAME.format(tag=project_name)),
        network='--network {}'.format(DOCKER_TEST_NETWOK_NAME.format(tag=project_name)),
        tag=DOCKER_TEST_SERVER_IMAGE.format(tag=project_name),
        volume='-v {app_path}:{docker_path}'.format(
            app_path=APP_PATH,
            docker_path=DOCKER_WORKING_PATH,
        ),
    )
    return os.system(command)


def docker_testserver_stop(project_name, exec=None):
    command = 'docker stop {name}>/dev/null'.format(
        name=DOCKER_TEST_SERVER_NAME.format(tag=project_name),
    )
    return os.system(command)


###############################################################################


def docker_network_create(project_name):
    command = 'docker network create {name}>/dev/null'.format(
        name=DOCKER_TEST_NETWOK_NAME.format(tag=project_name),
    )
    return os.system(command)


def docker_network_clean(project_name):
    command = 'docker network rm -f {name}>/dev/null'.format(
        name=DOCKER_TEST_NETWOK_NAME.format(tag=project_name),
    )
    return os.system(command)


###############################################################################


def action_clean(project_name):
    docker_testclient_image_clean(project_name)
    docker_testserver_image_clean(project_name)
    return 0


def action_migrate(project_name):
    return docker_testserver_run(project_name, exec='python manage.py migrate')


def action_migrations(project_name):
    return docker_testserver_run(project_name, exec='python manage.py makemigrations')


def action_restore(project_name):
    return docker_testserver_run(
        project_name,
        exec="/bin/bash -c '/bin/chown -vR $(stat -c %u .):$(stat -c %g .) .'"
    )


def action_runserver(project_name):
    return docker_testserver_run(project_name)


def action_shell(project_name):
    return docker_testserver_run(project_name, exec='/bin/bash')


def action_startproject(project_name):
    if project_name == 'replace_me_with_your_project_name':
        sys.exit('Error: Update the PROJECT_NAME in the Makefile.')
    docker_testserver_run(project_name, exec='django-admin startproject {name} .'.format(name=project_name))
    action_restore(project_name)
    return 0


def action_test(project_name):
    docker_network_create(project_name)
    docker_testserver_run_daemon(project_name)
    target=docker_testserver_address(project_name)
    result = docker_testclient_run(
        project_name,
        server_host=target,
        server_port=8000,
        exec='python tests/functional_tests.py',
    )
    docker_testserver_stop(project_name)
    docker_network_clean(project_name)
    return result


def action_unittest(project_name):
    return docker_testserver_run(project_name, exec='python manage.py test')


###############################################################################

if not os.path.join(WORKING_PATH, 'Makefile.d/make.py') == SCRIPT_PATH:
    sys.exit('Error: Run this script from project root (with Makefile.d sub-directory.)')

if __name__ == '__main__':
    DISPATCH = {
        'clean': action_clean,
        'migrate': action_migrate,
        'migrations': action_migrations,
        'restore': action_restore,
        'runserver': action_runserver,
        'shell': action_shell,
        'startproject': action_startproject,
        'test': action_test,
        'unittest': action_unittest,
    }
    arguments = docopt(__doc__, version='make.py 0.1')
    action_name = arguments['<action>']
    project_name = arguments['<project>']
    action = DISPATCH.get(action_name)
    if not action:
        sys.exit('Error: Unknown action "{}"'.format(action_name))
    else:
        sys.exit(action(project_name))

