from datetime import datetime
from rest_framework import serializers
from .models import Room, RoomImage, Booking
from rest_framework.response import Response
from .utility import is_room_available
from django.utils.timezone import now


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image']


class RoomSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['id',
                  'room_number',
                  'price_per_night',
                  'capacity',
                  'description',
                  'included_services',
                  'main_image',
                  'images',
                  ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'room', 'check_in',
            'check_out', 'total_price', 'status', 'booked_at'
        ]
        read_only_fields = ['user', 'total_price', 'status', 'booked_at']

    def validate(self, data):
        check_in = data['check_in']
        check_out = data['check_out']
        room = data['room']

        if check_in < now().date():
            raise serializers.ValidationError(
                {'check_in': 'you can not select past check in days'}
            )
        if check_out <= check_in:
            raise serializers.ValidationError(
                {"check_out": "Check-out must be after check-in"}
            )

        if not is_room_available(room, check_in, check_out):
            raise serializers.ValidationError(
                {"room": "Room is not available for selected dates"}
            )

        return data

    def create(self, validated_data):
        user = self.context['request'].user
        room = validated_data['room']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        days = (check_out - check_in).days
        total_price = days * room.price_per_night

        booking = Booking.objects.create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
        )
        return booking
