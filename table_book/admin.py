from django.contrib import admin
from table_book.models import Tables, Application, Booking


@admin.register(Tables)
class TablesAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    pass