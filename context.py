import troggle.settings as settings

def settingsContext(request):
    return { 'settings':settings }