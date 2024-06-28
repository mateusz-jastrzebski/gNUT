import os
import random
import string
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser if none exists'

    def handle(self, *args, **options):
        user = get_user_model()
        if not user.objects.filter(is_superuser=True).exists():
            username = 'admin'
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
            email = 'admin@example.com'
            user.objects.create_superuser(username=username, email=email, password=password)
            with open('./superuser.txt', 'w') as f:
                f.write(f'Username: {username}\nPassword: {password}\n')
            print('[AUTH] Created superuser with credentials inside superuser.txt')
        else:
            print('[AUTH] Superuser exists, skipping creating a new one.')
