<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

#### Features
key | default value | env
-|-|-
`BROKER_URL` | `None` | `DJANGO_BROKER_URL`
`BROKER_CONNECTION_TIMEOUT` | `4.0` | `DJANGO_BROKER_CONNECTION_TIMEOUT`
`BROKER_CONNECTION_RETRY` | `True` | `DJANGO_BROKER_CONNECTION_RETRY`
`BROKER_CONNECTION_MAX_RETRIES` | `100` | `DJANGO_BROKER_CONNECTION_MAX_RETRIES`
`CELERY_ACCEPT_CONTENT` | `['application/json']` | `DJANGO_CELERY_ACCEPT_CONTENT`
`CELERY_ACKS_LATE` | `False` | `DJANGO_CELERY_ACKS_LATE`
`CELERY_CREATE_MISSING_QUEUES` | `True` | `DJANGO_CELERY_CREATE_MISSING_QUEUES`
`CELERY_ENABLE_UTC` | `True` | `DJANGO_CELERY_ENABLE_UTC`
`CELERY_RESULT_SERIALIZER` | `'json'` | `DJANGO_CELERY_RESULT_SERIALIZER`
`CELERY_TASK_SERIALIZER` | `'json'` | `DJANGO_CELERY_TASK_SERIALIZER`
`CELERY_TIMEZONE` | `'UTC'` | `DJANGO_CELERY_TIMEZONE`
`CELERY_IMPORTS` | `[]` | `DJANGO_CELERY_IMPORTS`
`CELERY_INCLUDE` | `[]` | `DJANGO_CELERY_INCLUDE`
`CELERYBEAT_SCHEDULER` | `celery.beat:PersistentScheduler` | `DJANGO_CELERYBEAT_SCHEDULER`
`CELERYBEAT_SCHEDULE_FILENAME` | `celerybeat-schedule` | `DJANGO_CELERYBEAT_SCHEDULE_FILENAME`
`CELERYBEAT_SYNC_EVERY` | `0` | `DJANGO_CELERYBEAT_SYNC_EVERY`

##### `settings.py`
```python
from django_configurations_celery import CeleryConfiguration

class Base(CeleryConfiguration,...):
```

##### `.env`
```bash
DJANGO_BROKER_URL=redis://localhost:6379/0
DJANGO_CELERY_IMPORTS=celery_app,tasks
```

#### Links
+   [django-configurations](https://github.com/jazzband/django-configurations)
+   [Celery configuration and defaults](https://docs.celeryproject.org/en/latest/userguide/configuration.html)

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>