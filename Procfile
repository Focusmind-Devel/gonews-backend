heroku config:set DISABLE_COLLECTSTATIC=1
web: gunicorn gonewsBack.wsgi --log-file -
heroku ps:scale web=1
release: python manage.py migrate
