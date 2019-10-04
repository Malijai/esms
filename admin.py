from django.contrib import admin
from . models import Ressource, Professionnels, Esms
# Register your models here.

admin.site.register(Professionnels)
admin.site.register(Ressource)
admin.site.register(Esms)
