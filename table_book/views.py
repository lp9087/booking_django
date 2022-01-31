from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from table_book.models import Tables, Queue, Booking
from table_book.serializers import TablesSerializer, QueueSerializer, BookingSerializer


class TablesViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TablesSerializer


class QueueViewSet(ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        date = request.data['date']
        beginning_time = request.data['beginning_time']
        ending_time = request.data["ending_time"]
        guests = request.data['guest']
        table_number = request.data['table_number']
        table = Tables.objects.filter(number=table_number).first()
        app = Queue.objects.filter(id=guests).first()
        booking = Booking.objects.filter(table_number=table_number, date=date)

        for book in booking:
            if str(book.beginning_time) <= beginning_time <= str(book.ending_time):
                return Response('Стол уже занят')
        if table:
            if app:
                app.status = True
                app.save()
            else:
                return Response('Нет данной записи в очереди')
            Booking.objects.create(table_number=table, guest=app, date=date, beginning_time=beginning_time,
                                   ending_time=ending_time)
            return Response(f'Бронирование стола {table_number} успешно выполнено',
                            status=status.HTTP_201_CREATED)
        else:
            return Response('Данный стол отсутствует')

    def delete(self, request, *args, **kwargs):
        data_guests = request.data['guest']
        data_table_number = request.data['table_number']
        table = Tables.objects.filter(number=data_table_number).first()
        app = Queue.objects.filter(id=data_guests).first()
        if table:
            Booking.objects.filter(table_number=table, guest=app).delete()
            if app:
                app.delete()
            else:
                return Response('Нет данной записи в очереди')
            return Response(f'Бронирование стола {data_table_number} закончено', status=status.HTTP_201_CREATED)
        else:
            return Response('Данный стол отсутствует')
