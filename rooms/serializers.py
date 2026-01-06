from rest_framework import serializers
from .models import Room, RoomImage, Booking


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
                  'is_available',
                  'description',
                  'included_services',
                  'main_image',
                  'images',
                  ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'check_in',
                  'check_out', 'total_price', 'status', 'booked_at']
        read_only_fields = ['user', 'total_price', 'status', 'booked_at']

    def create(self, validated_data):
        user = self.context['request'].user
        room = validated_data['room']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        days = (check_out-check_in).days
        total_price = days*room.price_per_night

        booking = Booking.objects.create(
            user=user,
            room=room,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
        )
        return booking
