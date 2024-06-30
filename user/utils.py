from .models import Sector, Position, User
from datetime import datetime


def fake_user(sector=None, rank=None):
    if sector:
        sector = Sector.objects.get(id=sector)
    if rank:
        rank = Position.objects.get(id=rank)
    user, created = User.objects.get_or_create(
        username=f'zahirauser{sector}',
        email='zahira_user@example.com',
        password='1',
        first_name='Zahira',
        last_name='User',
        is_active=True,
        rank = rank,
        date_of_birth=datetime.strptime('1990-01-01', '%Y-%m-%d'),
        sector=sector
    )
    user.set_password('1')
    user.save()
    return user
