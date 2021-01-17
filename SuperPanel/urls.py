from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

	# SUPER USER PANEL
    path('home', views.home, name='home'),
    path('login', views.loginUser, name='loginUser'),
    path('signup', views.signup, name='signup'),
    path('forgot-password', views.forgotpass, name='forgotpass'),
    path('logout', views.logout, name='logout'),
    path('create-company', views.create_company, name='create_company'),
    path('super-admin-login', views.super_admin_login, name='super_admin_login'),
    path('send-credentails/<id>', views.send_credentails, name='send_credentails'),
    path('change-employee-status/<id>', views.change_employee_status, name='change_employee_status'),
    path('exportData/', views.exportData, name='exportData'),
    path('bulk-upload', views.bulk_upload, name='bulk_upload'),
    path('save-upload/', views.save_upload, name='save_upload'),
    path('bulk_upload_status', views.bulk_upload_status, name='bulk_upload_status'),
    path('edit-company', views.edit_company, name='edit_company'),
    path('save-company/', views.save_company, name='save_company'),
    path('change-company-status/<id>', views.change_company_status, name='change_company_status'),
    path('view-company', views.view_company, name='view_company'),

   ]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
