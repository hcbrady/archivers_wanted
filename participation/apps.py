from django.apps import AppConfig


class ParticipationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'participation'
    def ready(self):
        print("ready self")
        import participation.signals
