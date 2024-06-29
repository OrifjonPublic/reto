from django.db.models import Count, Q
from django.conf import settings
from .models import Task
from user.models import User, Position, Sector


#asosiy sahifa uchun
def all_stats_main():
    xodim = Position.objects.get(name=settings.EMPLOYEE)
    manager = Position.objects.get(name=settings.MANAGER)
    admin = Position.objects.get(name=settings.ASSIST)
    director = Position.objects.get(name=settings.BOSS)

    total_tasks = Task.objects.filter(is_active=True).count()

    all_tasks = Task.objects.filter(is_active=True)

    # Har bir status bo'yicha vazifalar sonini hisoblash
    tasks_by_status = Task.objects.filter(assigned_to__rank__in=[xodim, manager]).filter(assigned_by__rank=director).values('status').annotate(total=Count('status'))

    doing_tasks = all_tasks.filter(status='doing').count()
    procent_doing = (doing_tasks / total_tasks) * 100 if total_tasks else 0
    # Bajarilgan vazifalar sonini hisoblash

    finished_tasks = all_tasks.filter(status='finished').count()
    procent_finished = (finished_tasks / total_tasks) * 100 if total_tasks else 0

    missed_tasks = all_tasks.filter(status='missed').count()
    procent_missed = (missed_tasks / total_tasks) * 100 if total_tasks else 0

    canceled_tasks = all_tasks.filter(status='canceled').count()
    procent_canceled = (canceled_tasks / total_tasks) * 100 if total_tasks else 0

    # Muhimligi yuqori bo'lgan tasklar soni
    # important_tasks = Task.objects.filter(label='eng muhim').count()

    # Statistikaning lug'at ko'rinishini yaratish

    main_stats = {
        'total_tasks': total_tasks,
        'doing_tasks': [doing_tasks, procent_doing],
        'finished_tasks': [finished_tasks, procent_finished],
        'missed_tasks': [missed_tasks, procent_missed],
        'canceled_tasks': [canceled_tasks, procent_canceled]
    }

    return main_stats



# ALL SECTOR STATS va ularning vazifalar statistikasi haqida ma'lumotni olish
def all_sector():
    sector_task_stats = (
            Sector.objects
            .annotate(
                total_tasks=Count('user__tasks_assigned_to', distinct=True),
                tasks_missed=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='missed')),
                tasks_doing=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='doing')),
                tasks_finished=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='finished')),
                tasks_canceled=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='canceled')),
            )
            .order_by('name')
            .values(
                'name', 'total_tasks', 'tasks_missed', 'tasks_doing',
                'tasks_finished', 'tasks_canceled'
            )
        )
    sector_stats_list = []
    for sector in sector_task_stats:
        sector_stats = {}
        
        sector_stats['name'] = sector['name']
        sector_stats['total'] = sector['total_tasks']
        
        procent = (sector['tasks_doing'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
        sector_stats['doing'] = sector['tasks_doing'], procent
        
        procent_m = (sector['tasks_missed'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
        sector_stats['missed'] = sector['tasks_missed'], procent_m
        
        procent_f = (sector['tasks_finished'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
        sector_stats['finished'] = sector['tasks_finished'], procent_f
        
        procent_c = (sector['tasks_canceled'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
        sector_stats['canceled'] = sector['tasks_canceled'], procent_c
        
        sector_stats_list.append(sector_stats)

    all_sector_stats = sector_stats_list
    return all_sector_stats


# Har bir sektor uchun vazifalarning umumiy statistikasini olish

def one_sector_stat(id):
    sector = (
            Sector.objects.filter(id=id)
            .annotate(
                total_tasks=Count('user__tasks_assigned_to', distinct=True),
                tasks_missed=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='missed')),
                tasks_doing=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='doing')),
                tasks_finished=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='finished')),
                tasks_canceled=Count('user__tasks_assigned_to', filter=Q(user__tasks_assigned_to__status='canceled')),
            )
            .order_by('name')
            .values(
                'name', 'total_tasks', 'tasks_missed', 'tasks_doing',
                'tasks_finished', 'tasks_canceled'
            )
        )
    sector = sector[0]
    sector_stats = {}
    
    sector_stats['name'] = sector['name']
    sector_stats['total'] = sector['total_tasks']
    
    procent = (sector['tasks_doing'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
    sector_stats['doing'] = sector['tasks_doing'], procent
    
    procent_m = (sector['tasks_missed'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
    sector_stats['missed'] = sector['tasks_missed'], procent_m
    
    procent_f = (sector['tasks_finished'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
    sector_stats['finished'] = sector['tasks_finished'], procent_f
    
    procent_c = (sector['tasks_canceled'] / sector['total_tasks']) * 100 if sector['total_tasks'] else 0
    sector_stats['canceled'] = sector['tasks_canceled'], procent_c
    return sector_stats


def all_employees_stat_():
    users = User.objects.filter(Q(rank__name=settings.EMPLOYEE) | Q(rank__name=settings.MANAGER))
    statistics = []

    for user in users:
        all_count = Task.objects.filter(assigned_to=user).filter(is_active=True).count()
        doing_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='doing').count()
        doing_procent =( doing_count / all_count)  * 100 if all_count else 0    
        finished_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='finished').count()
        finished_procent =(finished_count / all_count)  * 100 if all_count else 0
        missed_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='missed').count()
        missed_procent =(missed_count / all_count)  * 100 if all_count else 0
        canceled_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='canceled').count()
        canceled_procent =(canceled_count / all_count)  * 100 if all_count else 0
        user_data = {
            'photo': user.photo.url,
            'user': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'total_tasks': all_count,
            'doing_count': doing_count,
            'doing_procent': doing_procent,
            'finished_count': finished_count,
            'finished_procent': finished_procent,
            'canceled_count': canceled_count,
            'canceled_procent': canceled_procent,
            'missed_count': missed_count,
            'missed_procent': missed_procent,
        }
        statistics.append(user_data)
    return statistics


def one_sector_employees(id):
    users = User.objects.filter(Q(rank__name=settings.EMPLOYEE) | Q(rank__name=settings.MANAGER)).filter(sector__id=id)
    statistics = []

    for user in users:
        all_count = Task.objects.filter(assigned_to=user).filter(is_active=True).count()
        doing_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='doing').count()
        doing_procent =( doing_count / all_count)  * 100 if all_count else 0    
        finished_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='finished').count()
        finished_procent =(finished_count / all_count)  * 100 if all_count else 0
        missed_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='missed').count()
        missed_procent =(missed_count / all_count)  * 100 if all_count else 0
        canceled_count = Task.objects.filter(is_active=True).filter(assigned_to=user, status='canceled').count()
        canceled_procent =(canceled_count / all_count)  * 100 if all_count else 0
        user_data = {
            'photo': user.photo.url,
            'user': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'total_tasks': all_count,
            'doing_count': doing_count,
            'doing_procent': doing_procent,
            'finished_count': finished_count,
            'finished_procent': finished_procent,
            'canceled_count': canceled_count,
            'canceled_procent': canceled_procent,
            'missed_count': missed_count,
            'missed_procent': missed_procent,
        }
        statistics.append(user_data)
    return statistics


# bir xodimning statistikasi
def one_employee_stat(id):
    all_tasks = Task.objects.filter(assigned_to__id=id)
    total_tasks = all_tasks.count()

    # Har bir status bo'yicha vazifalar sonini hisoblash
    tasks_by_status = all_tasks.values('status').annotate(total=Count('status'))
    doing_tasks = all_tasks.filter(status='doing').count()
    procent_doing = (doing_tasks / total_tasks) * 100 if total_tasks else 0
    # Bajarilgan vazifalar sonini hisoblash
    finished_tasks = all_tasks.filter(status='finished').count()
    procent_finished = (finished_tasks / total_tasks) * 100 if total_tasks else 0
    missed_tasks = all_tasks.filter(status='missed').count()
    procent_missed = (missed_tasks / total_tasks) * 100 if total_tasks else 0
    canceled_tasks = all_tasks.filter(status='canceled').count()
    procent_canceled = (canceled_tasks / total_tasks) * 100 if total_tasks else 0
    
    l = {
        'name': User.objects.get(id=id).username,
        'barcha': total_tasks,
        'bajarilgan': (doing_tasks, procent_doing),
        'tugatilgan': (finished_tasks, procent_finished),
        'bajarilmagan': (missed_tasks, procent_missed),
        'bekor qilingan': (canceled_tasks, procent_canceled)

    }
    return l