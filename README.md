# realgram

### teck stack

-  Django
-  Django rest framework
-  Postgresql

### Running the application

create a virtual enviornment

```console
python3 -m venv env
source env/bin/activate
```

install all required packages

```console
pip install -r requirements.txt
```

run migrations (if required)

```console
python manage.py makemigrations
python manage.py migrate
```

change database settings in settings.py file

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<your_db_name>',
        'USER': '<your_db_user>',
        'PASSWORD': '<your_db_user\'s_password>',
        'HOST': '<db_host>',
        'PORT': '<port_for_db>',
    }
}
```

run celery and redis servers

```console
redis-server &
celery --app=config.celery:app worker --loglevel=INFO --pidfile=celery.pid
```

start the application

```console
python manage.py runserver
```
