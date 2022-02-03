from rest_framework import serializers

from table_book.models import Tables, Queue, Booking


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):

    guest = serializers.CharField(source="guest.name")
    guest_number = serializers.CharField(source="guest.guest_number")
    guest_phone_number = serializers.CharField(source="guest.phone_number")
    table = serializers.CharField(source="table_number.number")

    class Meta:
        model = Booking
        fields = '__all__'


class TablesSerializer(serializers.ModelSerializer):
    booking = serializers.SerializerMethodField()

    def get_booking(self, instance):
        return instance.table.all().first() is not None

    class Meta:
        model = Tables
        fields = '__all__'

