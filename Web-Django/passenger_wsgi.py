import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.insert(0, "/home/u1641559/capstone2022")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EZDiagnose.settings')

application = get_wsgi_application()
