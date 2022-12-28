from django.contrib import admin
from apis.models import Movie, Screen, Show, Seat, Booking


# Register your models here.

admin.site.register(Movie)
admin.site.register(Screen)
admin.site.register(Show)
admin.site.register(Seat)
admin.site.register(Booking)
