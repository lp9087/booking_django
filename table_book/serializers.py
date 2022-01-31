from rest_framework.serializers import ModelSerializer

from table_book.models import Tables, Queue, Booking


class TablesSerializer(ModelSerializer):
    class Meta:
        model = Tables
        fields = '__all__'


class QueueSerializer(ModelSerializer):
    class Meta:
        model = Queue
        fields = '__all__'


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

