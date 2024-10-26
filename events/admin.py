from django.contrib import admin
from events.models import Evento


# Registro do modelo evento no admin
admin.site.register(Evento)