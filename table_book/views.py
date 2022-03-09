from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from braces.views import CsrfExemptMixin
from table_book.models import Tables, Queue, Booking
from table_book.serializers import TablesSerializer, QueueSerializer, BookingSerializer
import aiohttp
from django.shortcuts import render
import time
import asyncio
import requests


class TablesAPIView(CsrfExemptMixin, ModelViewSet):
    authentication_classes = []
    queryset = Tables.objects.all()
    serializer_class = TablesSerializer


class QueueViewSet(CsrfExemptMixin, ModelViewSet):
    authentication_classes = []
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer


class App_for_book(CsrfExemptMixin, ModelViewSet):
    authentication_classes = []
    queryset = Queue.objects.filter(status=False)
    serializer_class = QueueSerializer


class BookingViewSet(CsrfExemptMixin, ModelViewSet):
    authentication_classes = []
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        beginning_time = request.data['beginning_time']
        ending_time = request.data["ending_time"]
        guests = request.data['guest']
        table_number = request.data['table_number']
        table = Tables.objects.filter(number=table_number).first()
        app = Queue.objects.filter(id=guests).first()
        booking = Booking.objects.filter(table_number=table_number, beginning_time=beginning_time,
                                         ending_time=ending_time)

        for book in booking:
            if str(book.beginning_time) <= beginning_time <= str(book.ending_time):
                return Response('Стол уже занят')
        if table:
            if app:
                app.status = True
                app.save()
            else:
                return Response('Нет данной записи в очереди')
            Booking.objects.create(table_number=table, guest=app, beginning_time=beginning_time,
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


#async def example(request):
#    async with aiohttp.ClientSession() as session:
#        async with session.get("https://pokeapi.co/api/v2/pokemon/1") as res:
#            data = await res.json()
#            print(data)
#
#    return render(
#        request,
#        "index.html",
#        {"data": data},
#    )

#def example(request):
#    starting_time = time.time()
#    pokemon_data = []
#
#    for num in range(1,101):
#        url = f"https://pokeapi.co/api/v2/pokemon/{num}"
#        res = requests.get(url)
#        pokemon = res.json()
#        pokemon_data.append(pokemon["name"])
#
#    count = len(pokemon_data)
#    total_time = time.time() - starting_time
#
#    return render(
#        request,
#        "index.html",
#        {"data": pokemon_data, "count": count, "time": total_time},
#    )


async def example(request):
    starting_time = time.time()
    pokemon_data = []

    async with aiohttp.ClientSession() as session:
        for num in range(1, 101):
            pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{num}"
            async with session.get(pokemon_url) as res:
                pokemon = await res.json()
                pokemon_data.append(pokemon["name"])

    count = len(pokemon_data)
    total_time = time.time() - starting_time

    return render(
        request,
        "index.html",
        {"data": pokemon_data, "count": count, "time": total_time},
    )


#async def get_pokemon(session, url):
#    async with session.get(url) as res:
#        data = await res.json()
#        return data
#
#
#async def example(request):
#    starting_time = time.time()
#    actions = []
#    pokemon_data = []
#
#    async with aiohttp.ClientSession() as session:
#        for num in range(1, 101):
#            url = f"https://pokeapi.co/api/v2/pokemon/{num}"
#            actions.append(asyncio.ensure_future(get_pokemon(session, url)))
#
#            result = await asyncio.gather(*actions)
#            for data in result:
#                pokemon_data.append(data)
#
#    count = len(pokemon_data)
#    total_time = time.time() - starting_time
#
#    return render(
#        request,
#        "index.html",
#        {"data": pokemon_data, "count": count, "time": total_time},
#    )


