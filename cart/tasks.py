from celery import shared_task


@shared_task
def backup_database():
    print('hiiiiiii')
    return True