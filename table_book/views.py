from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from table_book.models import Tables, Application, Booking
from table_book.serializers import TablesSerializer, ApplicationSerializer, BookingSerializer


class TablesViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TablesSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class AppBookingViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class AppWithBookViewSet(ModelViewSet):
    queryset = Application.objects.filter(status=True)
    serializer_class = ApplicationSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        guest = request.data.get('guest')
        app_table = request.data.get('table_number')
        try:
            book_table = Tables.objects.get(id=app_table['id'])
            book_guest = Application.objects.get(id=guest['id'])
        except BaseException as e:
            return Response(e.args, status=status.HTTP_400_BAD_REQUEST)

        if book_table.status:
            book_table.status = False
            book_table.save()
        else:
            return Response('Стол занят')
        Booking.objects.create(table_number_id=book_table.id, guest_id=book_guest.id)
        book_guest.status = True
        book_guest.save()
        return Response(f'Бронирование стола {book_table} успешно выполнено', status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        data_guets = request.data['guest']
        data_table_number = request.data['table_number']
        table = Tables.objects.filter(number=data_table_number).first()
        app = Application.objects.filter(id=data_guets).first()
        if table:
            if not table.status:
                table.status = True
                table.save()
                Booking.objects.filter(table_number=table, guest=app).delete()
                if app:
                    app.delete()
                else:
                    return Response('Нет данной записи в очереди')
                return Response(f'Бронирование стола {data_table_number} закончено', status=status.HTTP_201_CREATED)
            else:
                return Response('Неккоректное бронирование - стол свободен')
        else:
            return Response('Данный стол отсутствует')










