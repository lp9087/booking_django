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


class AppWithoutBookViewSet(ModelViewSet):
    queryset = Application.objects.filter(status=False)
    serializer_class = ApplicationSerializer


class FreeTablesViewSet(ModelViewSet):
    queryset = Tables.objects.filter(status=True)
    serializer_class = TablesSerializer


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

    def destroy(self, request, *args, **kwargs):
        book_guest = Booking.objects.get(guest_id=kwargs.get('pk'))
        app_guest = Application.objects.get(id=kwargs.get('pk'))
        table = Booking.objects.select_related('table_number').get(guest_id=kwargs.get('pk')).table_number

        book_guest.delete()

        app_guest.delete()

        table.status = True
        table.save()
        return Response(f'Удаление брони успешно выполнено', status=status.HTTP_204_NO_CONTENT)







