# TDD with Django & Selenium in Docker
Quickly get started with Django & TDD using Docker & Selenium.

```
docker-django-selenium-tdd$ make help-all
---  Replace Me With Your Project Title  ---
Please use 'make <TARGET>' where <TARGET> is one of:
 help                   Show this dialogue. (Use help-all for development targets.)
 migrate                Run 'python manage.py migrate'
 migrations             Run 'python manage.py makemigrations'
 runserver              Run the development server.
 shell                  Drop into a bash shell on a container.
 test                   Run functional tests.
 unittest               Run unit tests.

Further <TARGET> options:
 print-banner           Used by each target to print the banner.
 clean                  Clean-up artifacts.
 restore                Restore file ownership to match parent dir.
 startproject           WARNING: Edit Makefile to set PROJECT_NAME
                        before running startproject!
```


## Quickstart
Bootstrap a new project in 3 steps:

1.  Start a new Django Project:
    *  Configure project title & shortname in the `Makefile`:
        *   Edit the `Makefile`
        *   `PROJECT_TITLE`: Set to e.g. "Inodo: Innovative Todo App"
        *   `PROJECT_NAME`: Set to e.g. "inodo", use lower-cases, no
            spaces, etc. This will be your app's django package name.
    *  Invoke Django-Admin startproject:
        *   Run:
            ```
            make startproject
            ```
        *   This triggers a build of the test-server docker image and
            runs `django-admin startproject $PROJECT_NAME` in a new
            container. The project, along with the `manage.py` file,
            is then moved into the `app` directory.
    *   Run the development server to ensure that your allowed-hosts
        is permissive:
        *   Run:
            ```
            make runserver
            ```
        *   Navigate to localhost at the stated port in your browser.
        *   Expect to see a Django error page about allowed hosts.
        *   Edit your projects `settings.py` file to add `'*'` for
            to `ALLOWED_HOSTS` for testing purposes.
        *   Re-run:
            ```
            make runserver
            ```
        *   Your browser should now show the Django start page.
2.  Prepare for TDD using selenium:
    *   Run the functional tests:
        ```
        make test
        ```
    *   In addition to the test-server image, a selenium & chrome
        ready test-client image is now built.
    *   The default test-suite looks for a stock title and so fails.
        You should edit `tests/functional_tests.py` to look for your
        project title.
3.  Make the test pass by starting an app:
    *   Drop into a shell on the test-server:
        ```
        make shell
        ```
    *   Create an app:
        ```
        python manage.py startapp frontend
        ```
    *   Install the app in your project's `settings.py` file.
    *   Setup urls, views & templates to return a title tag to pass
        the failing test.


## Command Reference

### make clean
Untags docker images and destroys any venvs that were created. Do
thise if you modify your `requirements.txt` files to trigger rebuilds.

### make help
Show help dialogue.

### make help-all
Show help dialogue for all commands.

### make migrate
Run `python manage.py migrate` (see also, [make migrations](#make-migrations).)

### make migrations
Run `python manage.py makemigrations` (see also, [make migrate](#make-migrate).)

### make restore
Restores file-ownership permissions. (These can sometimes get muddled by docker.)

### make runserver
Run the development server.

### make shell
Drop into a bash shell on the test-server container. (Useful for running e.g.
`python manage.py` or `django-admin` commands.

### make startproject
Runs `django-admin startprojet` using the PROJECT_NAME variable at the top of
the `Makefile`

    WARNING: Edit Makefile to set PROJECT_NAME var
    before running startproject!

### make test
Run the functional tests. The test-server is launched in one container, and
the selenium test-client in another. `tests/functional_tests.py` is then
run in the test-client.

### make unittest
Run `python manage.py test`, triggering the test-suits in your django apps.

