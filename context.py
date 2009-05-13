import troggle.settings as settings

def settingsContext(request):
    return { 'settings.MEDIA_URL':settings.MEDIA_URL,
                 'settings.URL_ROOT':settings.URL_ROOT,
		 'settings.ADMIN_MEDIA_PREFIX':settings.ADMIN_MEDIA_PREFIX,
		 'settings.SVX_URL':settings.SVX_URL }