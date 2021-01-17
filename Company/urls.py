from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

	# COMPANY USER PANEL
    path('company-users', views.company_users, name='company_users'),
    path('change-company-status/<id>', views.change_company_status, name='change_company_status'),

   ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
