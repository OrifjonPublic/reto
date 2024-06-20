from django.utils import timezone
from .models import TaskHistory


def change_user_sector(user, new_sector, tasks_to_new_sector, tasks_to_old_sector=None):
    old_sector = user.sector
    user.sector = new_sector
    user.save()

    for task in tasks_to_new_sector:
        task.sector = new_sector
        task.save()
        TaskHistory.objects.create(
            task=task,
            changed_by=user,
            old_sector=old_sector,
            new_sector=new_sector,
            change_date=timezone.now()
        )

    for task in tasks_to_old_sector:
        TaskHistory.objects.create(
            task=task,
            changed_by=user,
            old_sector=old_sector,
            new_sector=old_sector,
            change_date=timezone.now()
        )
    return True