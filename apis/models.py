from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Movie(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Screen(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    time = models.DateTimeField()

    def __str__(self):
        return self.name

    @property
    def name(self):
        return f"{self.movie.name}: {self.time}"

    @property
    def get_available_seats(self):
        if self.bookings.exists():
            booked_seats = self.bookings.values_list('seat_id')
            return Seat.objects.exclude(id__in=booked_seats)
        return Seat.objects.all()


class Seat(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Booking(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')

    def __str__(self):
        return f"show:{self.show}-seat:{self.seat}-user_id:{self.user_id}"
