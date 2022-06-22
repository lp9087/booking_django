from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from table_book.models import Tables, Application, Booking


class TablesSerializer(ModelSerializer):
    class Meta:
        model = Tables
        fields = ['id', 'number', 'seats', 'status']


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'table_number', 'guest']


class ApplicationSerializer(ModelSerializer):
    booking = BookingSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'name', 'datetime', 'guest_number', 'phone_number', 'note', 'status', 'booking']

