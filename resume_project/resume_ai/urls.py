# resume_ai/urls.py
from django.urls import path
from . import views  # Ensure this import exists

urlpatterns = [
    path('', views.dashboard, name='dashboard'),  # Dashboard is the homepage
    path('upload/', views.upload_resume, name='upload_resume'),
    path('generate/<int:resume_id>/', views.generate_cover, name='generate_cover'),
    path('edit/<int:cover_id>/', views.edit_cover, name='edit_cover'),
    path('download/<int:cover_id>/', views.download_cover, name='download'),
]