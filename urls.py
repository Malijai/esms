from django.urls import path, re_path
from .views import faitinstitution, ressource_new, RessourceDetail, rlisting, ressource_edit, bilan_province


urlpatterns = [
    path('code/<int:pk>/', faitinstitution, name='Faitinstitution'),
    re_path(r'^code/(?P<pk>[-\w]+)/(?P<choix>[\w]*)/$', faitinstitution, name='Faitinstitution'),
    re_path(r'^code/(?P<pk>[-\w]+)/(?P<choix>[\w]*)/(?P<histoire>[\w]*)/$', faitinstitution, name='Faitinstitution'),
    path('ressource/new/', ressource_new, name='ressource_new'),
    path('ressource/<int:pk>/edit/', ressource_edit, name='ressource_edit'),
    path('ressource/<int:pk>/', RessourceDetail.as_view(), name='ressource_detail'),
    path('bilanr/', bilan_province, name='ressource_bilan'),
    path('', rlisting, name='listeressources'),
]