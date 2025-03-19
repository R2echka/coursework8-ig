from celery import shared_task

from habbits.services import send_telegram_message


@shared_task
def habbit_remind(habbit):
    message = f'Напоминание про привычку "{habbit}"'
    if habbit.is_enjoyable:
        send_telegram_message(habbit.owner.tg_id, message)
    else:
        message += f", также не забудьте про награду {habbit.reward if habbit.reward else habbit.related_message}"
        send_telegram_message(habbit.owner.tg_id, message)
