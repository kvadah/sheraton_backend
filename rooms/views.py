from django.shortcuts import render
from .serializers import RoomImageSerializer, RoomSerializer
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
