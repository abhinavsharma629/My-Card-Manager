from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

	# EMPLOYEE USER PANEL
    path('edit-profile', views.edit_profile, name='edit_profile'),
    path('view-profile', views.view_profile, name='view_profile'),
    path('create_vcf', views.create_vcf, name='create_vcf'),

   ]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
