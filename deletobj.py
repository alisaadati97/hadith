import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hadith.settings')
django.setup()

from scrape.models import Hadith , Teller

for h in Hadith.objects.all():
    h.delete()
for t in Teller.objects.all():
    t.delete()


