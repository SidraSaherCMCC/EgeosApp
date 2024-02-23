from datetime import datetime
from  egeosapp.models import DateRequestPayload

class ParseDateTime():
    def parse_datetime(date_time_string):
        # Parse the string to a datetime object
        date_object = datetime.strptime(date_time_string, '%Y-%m-%dT%H:%M:%S.%fZ')

        # Extract year, month, day, hour, and minute components
        year = date_object.year
        two_digit_year = "{:02d}".format(year % 100)
        month = date_object.month
        two_digit_month = "{:02d}".format(month)
        day = date_object.day
        two_digit_day = "{:02d}".format(day)
        hour = date_object.hour
        two_digit_hour = "{:02d}".format(hour)
        minute = date_object.minute
        two_digit_minute = "{:02d}".format(minute)

        # Output the parsed components
        print("Year:", year)
        print("Month:", month)
        print("Day:", day)
        print("Hour:", hour)
        print("Minute:", minute)

        # Create and return the DateRequestPayload object
        dr_payload = DateRequestPayload(two_digit_year, two_digit_month, two_digit_day, two_digit_hour, two_digit_minute)
        return dr_payload