from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('create/', views.create, name="create"),
    path('join/', views.join, name="join"),
    path('createRoom/', views.createRoom, name='createRoom'),
    path('joinRoom/', views.joinRoom, name='joinRoom'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('saveContent/',views.save_content,name="saveContent"),
    path('document/<str:room>/',views.editor,name='editor'),    
    
]