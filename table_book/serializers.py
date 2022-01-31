from rest_framework.serializers import ModelSerializer

from table_book.models import Tables, Application, Booking


class TablesSerializer(ModelSerializer):
    class Meta:
        model = Tables
        fields = '__all__'


class ApplicationSerializer(ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

