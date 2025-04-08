import json
from datetime import datetime, timedelta

import requests
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import BOT_TOKEN


def send_telegram_message(id, message):
    params = {
        "text": message,
        "chat_id": id,
    }
    return requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", params=params
    )


def habbit_reminder(habbit):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=habbit.periodicity,
        period=IntervalSchedule.DAYS,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name="Habbit reminder",
        task="habbits.tasks.habbit_remind",
        kwargs=json.dumps(
            {
                "be_careful": True,
            }
        ),
        expires=datetime.now() + timedelta(seconds=habbit.time_to_complete),
    )
