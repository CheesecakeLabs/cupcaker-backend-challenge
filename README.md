[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Boilerplate project using Django and Django REST Framework.
Currently supporting only Python 3.x.

**IMPORTANT**:
Docker Compose is used _just_ for development environment. The Dockerfile works without it.

## How to install with Pyenv

```bash
$ pyenv virtualenv 3.8.0 <CupcakerChallenge>
$ pyenv activate <CupcakerChallenge>
$ pip install Django==2.2.7
$ django-admin.py startproject \
    --template=https://github.com/CheesecakeLabs/django-drf-boilerplate/archive/master.zip \
    <CupcakerChallenge> .
$ pip install -r src/config/requirements/dev.txt
$ python src/manage.py runserver
```

## How to install with Docker Compose

```bash
$ django-admin.py startproject \
  --template=https://github.com/CheesecakeLabs/django-drf-boilerplate/archive/master.zip \
  <CupcakerChallenge> .
$ docker-compose up
```

## Install Black code formatter to your editor

Check code syntax and style before committing changes.

Pre-commit hook may be installed using the following steps:

```bash
$ pip install -r src/requirements/dev.txt
$ pre-commit install
```

Or run it manually:

```bash
$ black .
```

## Database

Running database on latest PostgreSQL Docker container running in the port `5432`. The connection is defined by the `dj-database-url` package. There's a race condition script to avoid running Django before the database goes up.

## Handling Business Error

```
from helpers.business_errors import BusinessException, EXAMPLE_ERROR
...
if logic_check:
    raise BusinessException(error_code=EXAMPLE_ERROR)
```

`BusinessException` extends `APIException` (Django Rest Framework) and `ValidationError` (Django), so it is handled by their middlewares by default.

## Docs

Let's face it, human memory sucks. Will you remember every detail that involves your project 6 months from now? How about when the pressure is on? A project with good documentation that explains all the facets, interactions and architectural choices means you and your teammates won't have to spend hours trying to figure it out later. You can find a template to get started [here](https://github.com/CheesecakeLabs/django-drf-boilerplate/wiki/Docs-Template).
