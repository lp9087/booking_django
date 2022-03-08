from django.db import models


class Tables(models.Model):
    number = models.IntegerField('Номер стола')
    seats = models.IntegerField('Количество мест')
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
    guest_number = models.IntegerField('Количество гостей')
    phone_number = models.IntegerField('Номер телефона')
    note = models.CharField('Примечание', max_length=255, blank=True, null=True)
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
