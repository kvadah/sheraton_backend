from django.shortcuts import render
from .serializers import RoomImageSerializer, RoomSerializer, BookingSerializer
from .models import Room, RoomImage
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
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


class BookRoomView(APIView):

    def post(self, request):
        serializer = BookingSerializer(data=request.data, context={'request': request}
                                       )
        if serializer.is_valid():
            room = serializer.validated_data['room']
            if not room.is_available:
                return Response({'error': 'Room is not available'}, status=440)
            serializer.save()
            room.is_available = False
            room.save
            return Response({'message': 'booked succesfully'},
                            status=status.HTTP_201_CREATED)
        return Response({'error': 'invalid data'},
                        status=status.HTTP_400_BAD_REQUEST)
