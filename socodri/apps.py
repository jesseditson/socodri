from django.apps import AppConfig
from django.conf import settings
#from facebookads.api import FacebookAdsApi


class SocoDRIConfig(AppConfig):
    name = 'socodri'
    verbose_name = 'Socialcode DR Insights'

    def ready(self):
        #FacebookAdsApi.init(settings.FB_APP_ID, settings.FB_APP_SECRET, settings.FB_ACCESS_TOKEN)
        pass
