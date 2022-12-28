from django.core.handlers import exception
from django.shortcuts import render
from rest_framework import viewsets, routers, status
from apis.models import Movie, Show, Booking
from apis.serializers import MovieSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction


class MovieViewset(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ShowViewset(viewsets.ViewSet):

    @action(detail=False, methods=['get'], name='Get Available Seats')
    def get_available_seats(self, request, pk=None):
        show_id = request.query_params.get('show_id')
        if show_id:
            show = Show.objects.get(id=show_id)
            available_seats_qs = show.get_available_seats
            available_seats_ids = available_seats_qs.values_list('id', flat=True)
            return Response({'available_seat_ids': list(available_seats_ids)})
        else:
            return Response({'msg': 'show_id not found'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='Book Seat')
    def book_seat(self, request, pk=None):
        try:
            show_id = request.data.get('show_id')
            seat_ids = request.data.get('seat_ids')
            user_id = request.user.id or 1
            if show_id and seat_ids:
                with transaction.atomic():
                    for seat_id in seat_ids:
                        if Booking.objects.filter(show_id=show_id, seat_id=seat_id).exists():
                            raise exception.BadRequest()
                        else:
                            Booking.objects.create(show_id=show_id, seat_id=seat_id, user_id=user_id)
                return Response({'msg': 'Booking Done'})
            else:
                return Response({'msg': 'show_id not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        except exception.BadRequest as e:
            return Response({'msg': 'All Seat is not available.'},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], name='Get User for Seat')
    def get_user_for_seat(self, request, pk=None):
        show_id = request.query_params.get('show_id')
        seat_id = request.query_params.get('seat_id')
        if seat_id and show_id:
            booking = Booking.objects.filter(show_id=show_id, seat_id=seat_id)
            if booking.exists():
                user = booking[0].user.username
                return Response({'username': user})
            else:
                return Response({'msg': 'booking not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'msg': 'show_id or seat_id not found'},
                            status=status.HTTP_400_BAD_REQUEST)


router = routers.DefaultRouter()
router.register(r'movies', MovieViewset, basename='movies')
router.register(r'', ShowViewset, basename='show')
