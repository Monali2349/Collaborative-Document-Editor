# # from django.urls import path
# # from .consumers import RealtimeEditorConsumer

# # websocket_urlpatterns = [
# #     path('ws/realtime_editor/', RealtimeEditorConsumer.as_asgi()),
# # ]
from django.urls import path
from . import consumers

websocket_urlpatterns=[
    path('ws/sc/<str:room>/',consumers.MySyncConsumer.as_asgi()),
    path('ws/ac/',consumers.MyAsyncConsumer.as_asgi()),
]