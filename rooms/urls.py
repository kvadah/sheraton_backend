from django.urls import path
from .views import CreateRoomView, GetRoomsView, BookRoomView, CheckOutView, getBookings, ExtendBooking, GetAvailableRooms, GetRoomDetailView
urlpatterns = [
    path('create_room/', CreateRoomView.as_view()),
    path('', GetRoomsView.as_view()),
    path('book/', BookRoomView.as_view()),
    path('staff/bookings/<int:booking_id>/check_out/', CheckOutView.as_view()),
    path('bookings/', getBookings.as_view()),
    path('bookings/<int:booking_id>/extend/', ExtendBooking.as_view()),
    path('available_rooms/', GetAvailableRooms.as_view()),
    path('<int:room_id>/', GetRoomDetailView.as_view())

]
