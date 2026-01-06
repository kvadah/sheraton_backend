from django.urls import path
from .views import CreateRoomView, GetRoomsView, BookRoomView
urlpatterns = [
    path('create_room/', CreateRoomView.as_view()),
    path('', GetRoomsView.as_view()),
    path('book/', BookRoomView.as_view()),

]
