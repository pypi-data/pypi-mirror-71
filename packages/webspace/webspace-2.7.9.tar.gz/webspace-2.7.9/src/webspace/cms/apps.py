from django.apps import AppConfig


class CmsConfig(AppConfig):
    name = 'webspace.cms'

    def ready(self):
        import pdb
        pdb.set_trace()
        pass
