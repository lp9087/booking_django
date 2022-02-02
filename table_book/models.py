from django.db import models


class Tables(models.Model):
    number = models.DecimalField('Номер стола', max_digits=4, decimal_places=0, unique=True)
    seats = models.DecimalField('Количество мест', max_digits=4, decimal_places=0)

    def __str__(self):
        return f'Стол {self.number}: {self.seats} места'

    class Meta:
        verbose_name = 'Стол'
        verbose_name_plural = 'Столы'


class Queue(models.Model):
    name = models.CharField('ФИО', max_length=255)
    guest_number = models.DecimalField('Количество гостей', max_digits=4, decimal_places=0)
    phone_number = models.DecimalField('Номер телефона', max_digits=11, decimal_places=0)
    datetime = models.DateTimeField('Время желаемого бронирования', auto_now=False, auto_now_add=False)
    note = models.CharField('Пожелания', max_length=255, blank=True, null=True)
    status = models.BooleanField('Статус заявки', default=False)

    def __str__(self):
        return f'Имя {self.name}, количество гостей {self.guest_number}, дата {self.datetime.date()}, время {self.datetime.time()}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Booking(models.Model):
    table_number = models.ForeignKey('Tables', on_delete=models.CASCADE, related_name='booking')
    guest = models.ForeignKey('Queue', on_delete=models.CASCADE, related_name='guest')
    beginning_time = models.DateTimeField('Время начала бронирования', auto_now=False, auto_now_add=False)
    ending_time = models.DateTimeField('Время конца бронирования', auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.guest.name}: {self.guest.guest_number} гостей'

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'
