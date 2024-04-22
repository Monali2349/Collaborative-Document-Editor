# from django.urls import path
# from . import views
# from .views import AddBlog

# urlpatterns = [
#     path("", views.dashboard, name="dashboard"),
#     path('create/', AddBlog.as_view(), name='create'),
    
# ]
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path('create/', views.create, name="create"),
    path('join/', views.join, name="join"),
    # path('doc_detail/<str:room>', views.room, name='room'),
    path('createRoom/', views.createRoom, name='createRoom'),
    path('joinRoom/', views.joinRoom, name='joinRoom'),
    # path('create/<str:group_name>/', views.create, name='create'),
  
    path('<str:room>/',views.editor,name='editor'),    
   
]