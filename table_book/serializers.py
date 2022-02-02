from rest_framework import serializers

from table_book.models import Tables, Queue, Booking


class TablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tables
        fields = '__all__'


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):

    guest = serializers.CharField(source="guest.name")
    guest_number = serializers.CharField(source="guest.guest_number")
    guest_phone_number = serializers.CharField(source="guest.phone_number")

    class Meta:
        model = Booking
        fields = '__all__'

