from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from table_book.models import Tables, Application, Booking
from table_book.serializers import TablesSerializer, ApplicationSerializer, BookingSerializer


class TablesViewSet(ModelViewSet):
    queryset = Tables.objects.all()
    serializer_class = TablesSerializer


class ApplicationViewSet(ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer


class BookingViewSet(ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        data_guets = request.data[0]['guest']
        data_table_number = request.data[0]['table_number']
        table = Tables.objects.filter(number=data_table_number).first()
        app = Application.objects.filter(id=data_guets).first()
        if table:
            if app:
                if table.status:
                    table.status = False
                    table.save()
                else:
                    return Response('Стол занят')
                app.status = True
                app.save()
            else:
                return Response('Нет данной записи в очереди')
            Booking.objects.create(table_number=table, guest=app)
            return Response(f'Бронирование стола {data_table_number} успешно выполнено', status=status.HTTP_201_CREATED)
        else:
            return Response('Данный стол отсутствует')

    def delete(self, request, *args, **kwargs):
        data_guets = request.data[0]['guest']
        data_table_number = request.data[0]['table_number']
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










