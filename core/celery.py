from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Создаем объект Celery
app = Celery('core')

# Задаем настройки Celery через конфигурацию Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживаем задачи в приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
