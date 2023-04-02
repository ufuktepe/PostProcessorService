from django.apps import AppConfig


class PostProcessorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'post_processor'

    def ready(self):
        """
        This runs only once at the beginning.
        """
        pass