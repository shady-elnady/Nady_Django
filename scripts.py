import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Config.settings")
django.setup()

from User.models import User

User.objects.create_user(
    "shady@gmail.com", "12345", username="shady", bio="this is shady"
)
User.objects.create_superuser("shady@gmail.com", "12345", username="shady")
