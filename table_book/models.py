from django.db import models
from django.db.models import SET_NULL


class Tables(models.Model):
    number = models.DecimalField('Номер стола', max_digits=4, decimal_places=0)
    seats = models.DecimalField('Количество мест', max_digits=4, decimal_places=0)
    status = models.BooleanField('Свободен', default=True)

    def __str__(self):
        return f'Стол {self.number}: {self.seats} места'

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'


class Application(models.Model):
    name = models.CharField('ФИО', max_length=255)
    date = models.DateField('Дата', auto_now=False, auto_now_add=False)
    time = models.TimeField('Время', auto_now=False, auto_now_add=False)
    guest_number = models.DecimalField('Количество гостей', max_digits=4, decimal_places=0)
    note = models.CharField('Примечание', max_length=255,blank=True, null=True)
    status = models.BooleanField('Статус заявки', default=False)

    def __str__(self):
        return f'Имя {self.name}, количество гостей {self.guest_number}, время {self.time}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Booking(models.Model):
    table_number = models.ForeignKey('Tables', on_delete=models.CASCADE, related_name='table')
    guest = models.ForeignKey('Application', on_delete=models.CASCADE, related_name='guest')

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
