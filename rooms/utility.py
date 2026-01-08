from .models import Booking
from datetime import date, timedelta
import calendar


def is_room_available(room,check_in,check_out):
    return not Booking.objects.filter(
        room=room,
        status__in=['reserved','checked_in'],
        check_in__lt=check_out,
        check_out__gt=check_in,
    ).exists()


def get_month_range(year, month):
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    return first_day, last_day


def expand_dates(start, end):
    current = start
    while current < end:
        yield current
        current += timedelta(days=1)
