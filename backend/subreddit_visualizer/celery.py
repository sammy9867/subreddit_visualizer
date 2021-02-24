from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "subreddit_visualizer.settings")

app = Celery("subreddit_visualizer")
app.config_from_object(__name__)

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'praw-every-monday-morning': {
        "task": "score.tasks.get_subreddits_every_monday",
        "schedule": crontab(minute=32)#crontab(hour=0, minute=5, day_of_week=1)
    }
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))