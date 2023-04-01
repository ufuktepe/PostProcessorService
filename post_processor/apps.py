from django.apps import AppConfig


class PostProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post_processor'

    def ready(self):
        print('Initialized...........')