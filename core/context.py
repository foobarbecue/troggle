from django.conf import settings
from core.models import Expedition

def troggle_context(request):
    return { 'settings':settings, 'Expedition':Expedition }