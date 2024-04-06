web: gunicorn DocumentManagementSystem.wsgi --log-file -
worker: celery -A DocumentManagementSystem worker -l info
beat: celery -A DocumentManagementSystem beat -l info
