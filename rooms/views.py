from datetime import datetime
from django.shortcuts import render
from .serializers import RoomImageSerializer, RoomSerializer, BookingSerializer
from .models import Room, RoomImage, Booking
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.utils.dateparse import parse_date
# Create your views here.


class CreateRoomView(APIView):
   # permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            room = serializer.save()
            images = request.FILES.getlist('images')
            for image in images:
                RoomImage.objects.create(
                    room=room,
                    image=image
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetRoomsView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True,)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAvailableRooms(APIView):
    def get(self, request):
        check_in = parse_date(request.query_params.get('check_in'))
        check_out = parse_date(request.query_params.get('check_out'))

        if not check_in or not check_out:
            return Response(
                {"error": "check_in and check_out are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if check_in >= check_out:
            return Response(
                {"error": "check_out must be after check_in"},
                status=status.HTTP_400_BAD_REQUEST
            )

        available_rooms = (Room.objects.exclude(
            bookings__status__in=['reserved', 'checked_in'],
            bookings__check_in__lt=check_out,
            bookings__check_out__gt=check_in,
        ).distinct()
        )
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)


class BookRoomView(APIView):

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request}
                                       )
        if serializer.is_valid():
            room = serializer.validated_data['room']
            if not room.is_available:
                return Response({'error': 'Room is not available'}, status=440)
            serializer.save()
            room.save
            return Response({'message': 'booked succesfully'},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CheckOutView(APIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({'error: invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.status != 'checked_in':
            return Response({'error': f'you can not check out from status "{booking.status}"'}, status=status.HTTP_400_BAD_REQUEST)
        booking.status = 'checked_out'
        booking.save()
        booking.room.is_available = True
        booking.room.save()
        return Response('checkedout successfully', status=status.HTTP_200_OK)


class getBookings(APIView):

    def get(self, request):
        user = request.user

        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)


class ExtendBooking(APIView):
    def post(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error: invalid request'}, status=status.HTTP_400_BAD_REQUEST)
        if booking.status != 'checked_in':
            return Response({'error': f'you can not extend booking before checking in'}, status=status.HTTP_400_BAD_REQUEST)

        check_out = request.data['check_out']
        try:
            check_out = datetime.strptime(check_out, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {'error': 'Invalid date format. Use YYYY-MM-DD'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if check_out < booking.check_out:
            return Response(
                {'error': f'you can not extend from  "{booking.check_out}" to "{check_out}" '},
                status=status.HTTP_400_BAD_REQUEST
            )
        booking.check_out = check_out
        days = (check_out-booking.check_in).days
        total_price = days*booking.room.price_per_night
        booking.total_price = total_price
        booking.save()
        return Response('successfully extended')
