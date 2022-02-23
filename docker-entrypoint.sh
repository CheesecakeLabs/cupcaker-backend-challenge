#!/bin/bash
set -e

if [ -n "$1" ]; then
    exec "$@"
fi

if [ "$ENV" = "development" ] ; then
    # Check Postgres database
    python docker/web/check_db.py
    pip install -r src/config/requirements/dev.txt
fi

python src/manage.py migrate                  # Apply database migrations
python src/manage.py collectstatic --noinput  # Collect static files

if [ "$ENV" = "development" ] ; then
    python src/manage.py runserver 0.0.0.0:8000
else
    # Prepare log files and start outputting logs to stdout
    mkdir -p /srv/logs/
    touch /srv/logs/gunicorn.log
    touch /srv/logs/access.log
    tail -n 0 -f /srv/logs/*.log &

    # Start Gunicorn processes
    echo Starting Gunicorn
    exec gunicorn core.wsgi \
        --bind 0.0.0.0:8000 \
        --chdir /usr/src/app/src \
        --workers 3 \
        --log-level=info \
        --log-file=/srv/logs/gunicorn.log \
        --access-logfile=/srv/logs/access.log
fi
