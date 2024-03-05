from django.urls import path
from . import views
from .views import AddBlog

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('create/', AddBlog.as_view(), name='create'),
]
