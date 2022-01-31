from django.contrib import admin
from table_book.models import Tables, Queue, Booking


@admin.register(Tables)
class TablesAdmin(admin.ModelAdmin):
    pass


@admin.register(Queue)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass