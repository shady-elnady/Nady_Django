from django.conf import settings
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

from django.urls import reverse_lazy
from django.shortcuts import redirect


class QRField(models.Field):
    def __init__(self, max_length=24, *args, **kwargs):
        self.max_length = max_length
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return "char(%s)" % self.max_length




class BarCodeField(models.CharField):
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('verbose_name', 'BarCode Code')
        kwargs['max_length'] = 24
        kwargs['primary_key'] = True
        # kwargs['choices'] = CurrencyChoices.choices

        myDate = datetime.now()
        # Give a format to the date
        # Displays something like: Aug. 27, 2017, 2:57 p.m.
        formatedDate = myDate.strftime("%Y-%m-%d %H:%M:%S")
        currentUser= get_user_model()
        if currentUser.is_staff:
            # Do something for authenticated users.
            user= currentUser.id
            # branch= settings.AUTH_USER_MODEL.branch
        else:
            # Do something for anonymous users.            
            return redirect(reverse_lazy('login'))

        kwargs['default'] = f"{user}-{formatedDate}"
        super().__init__(*args, **kwargs)


class CustomDateTimeField(models.DateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)
        if val:
            val.replace(microsecond=0)
            return val.isoformat()
        return ''



"""
    %a	Locale’s abbreviated weekday name.
    %A	Locale’s full weekday name.
    %b	Locale’s abbreviated month name.
    %B	Locale’s full month name.
    %c	Locale’s appropriate date and time representation.
    %d	Day of the month as a decimal number [01,31].
    %H	Hour (24-hour clock) as a decimal number [00,23].
    %I	Hour (12-hour clock) as a decimal number [01,12].
    %j	Day of the year as a decimal number [001,366].
    %m	Month as a decimal number [01,12].
    %M	Minute as a decimal number [00,59].
    %p	Locale’s equivalent of either AM or PM.
    %S	Second as a decimal number [00,61].
    %U	Week number of the year (Sunday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Sunday are considered to be in week 0.
    %w	Weekday as a decimal number [0(Sunday),6].
    %W	Week number of the year (Monday as the first day of the week) as a decimal number [00,53]. All days in a new year preceding the first Monday are considered to be in week 0.
    %x	Locale’s appropriate date representation.
    %X	Locale’s appropriate time representation.
    %y	Year without century as a decimal number [00,99].
    %Y	Year with century as a decimal number.
    %Z	Time zone name (no characters if no time zone exists).
    %%	A literal '%' character.


    Format
        Character	Description	                                                    Example

        %a	        Abbreviated day name.	                                        Fri, Sun
        %A	        Full name of the day.	                                        Friday, Sunday
        %B	        Full name of the month.	                                        June, July
        %b	        Abbreviated month name.	                                        Jan, Feb
        %m	        Month as a zero-padded decimal number.	                        06, 10
        %d	        Day of the month as a zero-padded decimal.	                    18, 31
        %y	        The year without century as a zero-padded decimal number.	    99, 22
        %Y	        The year with century as a decimal number.	                    1999, 2022
        %j	        Day of the year as a zero-padded decimal number.	            135, 365
        %U	        Week number of the year. The first day as Sunday.	            28, 53
        %W	        Week number of the year. The first day as Monday.	            00, 53
        %x	        Locale’s appropriate date representation.	                    12/31/18


        '%Y-%m-%d %H:%M:%S',    # '2006-10-25 14:30:59'
        '%Y-%m-%d %H:%M',       # '2006-10-25 14:30'
        '%Y-%m-%d',             # '2006-10-25'
        '%m/%d/%Y %H:%M:%S',    # '10/25/2006 14:30:59'
        '%m/%d/%Y %H:%M',       # '10/25/2006 14:30'
        '%m/%d/%Y',             # '10/25/2006'
        '%m/%d/%y %H:%M:%S',    # '10/25/06 14:30:59'
        '%m/%d/%y %H:%M',       # '10/25/06 14:30'
        '%m/%d/%y'              # '10/25/06'

"""