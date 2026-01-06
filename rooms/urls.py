from django.urls import path
from .views import CreateRoomView,GetRoomsView
urlpatterns =[
    path('create_room/',CreateRoomView.as_view()),
    path('',GetRoomsView.as_view()),

]