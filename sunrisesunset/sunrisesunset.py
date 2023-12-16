# -*- coding: utf-8 -*-
#
# sunrisesunset.py
#
"""
This code is valid for dates from 1901 to 2099, and will not calculate
sunrise/sunset times for latitudes above/below 63/-63 degrees.

No external packages are used when using the class SunriseSunset. If you
run the tests you will need to install pytz, geopy, and timezonefinder as
shown below or use your package installer if it's available.
----------------------------------

Contributions by:
   Darryl Smith -- Noticed a bug with atan fixed with atan2.
"""
__docformat__ = "restructuredtext en"


import datetime
from math import degrees, radians, atan2, cos, sin, pi, sqrt, fabs


class SunriseSunset:
    """
    This class determines the sunrise and sunset for zenith standards for the
    given day. It can also tell you if the given time is during the nigh or
    day.
    """
    __ZENITH = {'official': -0.833,
                'civil': -6.0,
                'nautical': -12.0,
                'amateur': -15.0,
                'astronomical': -18.0}

    def __init__(self, date:datetime, lat:float, lon:float,
                 zenith:str='official') -> None:
        """
        Set the values for the sunrise and sunset calculation.

        :param date: A localized datetime object that is timezone aware.
        :type date: datetime
        :param lat: The latitude.
        :type lat: float
        :param lon: The longitude.
        :type lon: float
        :param zenith: The zenith name.
        :type zenith: str
        """
        if not isinstance(date, datetime.datetime) or date.tzinfo is None:
            msg = "The date must be a datetime object with timezone info."
            raise ValueError(msg)

        if zenith not in self.__ZENITH:
            msg = (f"Invalid zenith name '{zenith}' must be one of: "
                   f"'{list(self.__ZENITH.keys())}'")
            raise ValueError(msg)

        if abs(lat) > 63:
            raise ValueError(f'Invalid latitude: {lat}')

        self.__date_local = date
        self.__lat = lat
        self.__lon = lon
        self.__zenith = zenith
        local_tuple = date.timetuple()
        utc_tuple = date.utctimetuple()
        self.__offset_utc = (local_tuple[3] - utc_tuple[3]) + \
                           (local_tuple[4] - utc_tuple[4]) / 60.0
        self.__sunrise = None
        self.__sunset = None
        self.__determine_rise_set()

    def is_night(self, collar:int=0) -> bool:
        """
        Check if it is day or night. If the 'collar' keyword argument is
        changed it will skew the results to either before or after the real
        sunrise and sunset. This is useful if lead and lag times are needed
        around the actual sunrise and sunset.

        .. note::

            If collar == 30 then this method will say it is daytime 30
            minutes before the actual sunrise and likewise 30 minutes after
            sunset it would indicate it is night.

        :keyword collar: The minutes before or after sunrise and sunset.
        :type collar: int
        :return: True if it is night else False if day.
        :rtype: bool
        """
        delta = datetime.timedelta(minutes=collar)
        return ((self.__sunrise - delta) > self.__date_local
                or self.__date_local > (self.__sunset + delta))

    @property
    def sun_rise_set(self) -> tuple:
        """
        Get the sunrise and sunset.

        :return: A C{datetime} object in a tuple (sunrise, sunset).
        :rtype: tuple
        """
        return self.__sunrise, self.__sunset

    def __determine_rise_set(self):
        """
        Determine both the sunrise and sunset.
        """
        year = self.__date_local.year
        month = self.__date_local.month
        day = self.__date_local.day
        # Ephemeris
        ephem2000day = (367 * year - (7 * (year + (month + 9) / 12) / 4) +
                        (275 * month / 9) + day - 730531.5)
        self.__sunrise = self.__determine_rise_or_set(ephem2000day, 1)
        self.__sunset = self.__determine_rise_or_set(ephem2000day, -1)

    def __determine_rise_or_set(self, ephem2000day:float, rs:int) -> datetime:
        """
        Determine either the sunrise or the sunset.

        :param ephem2000day: The Ephemeris from the beginning of the
                             21st century.
        :type ephem2000day: float
        :param rs: The factor that determines either sunrise or sunset where
                   1 equals sunrise and -1 sunset.
        :type rs: int
        :return: Either the sunrise or sunset as a C{datetime} object.
        """
        utold = pi
        utnew = 0
        altitude = self.__ZENITH[self.__zenith]
        sin_alt = sin(radians(altitude))    # solar altitude
        sin_phi = sin(radians(self.__lat))  # viewer's latitude
        cos_phi = cos(radians(self.__lat))  #
        lon = radians(self.__lon)           # viewer's longitude
        ct = 0
        #print(rs, ephem2000day, sin_alt, sin_phi, cos_phi, lon)

        while fabs(utold - utnew) > 0.001 and ct < 35:
            ct += 1
            utold = utnew
            days = ephem2000day + utold / (2 * pi)
            t = days / 36525
            # The magic numbers are orbital elements of the sun.
            l = self.__get_range(4.8949504201433 + 628.331969753199 * t)
            g = self.__get_range(6.2400408 + 628.3019501 * t)
            ec = 0.033423 * sin(g) + 0.00034907 * sin(2 * g)
            lam = l + ec
            e = -1 * ec + 0.0430398 * sin(2 * lam) - 0.00092502 * sin(4 * lam)
            obl = 0.409093 - 0.0002269 * t
            delta = sin(obl) * sin(lam)
            delta = atan2(delta, sqrt(1 - delta * delta))
            gha = utold - pi + e
            cosc = (sin_alt - sin_phi * sin(delta)) / (cos_phi * cos(delta))

            if cosc > 1:
                correction = 0
            elif cosc < -1:
                correction = pi
            else:
                correction = atan2((sqrt(1 - cosc * cosc)), cosc)

            #print(cosc, correction, utold, utnew)
            utnew = self.__get_range(utold - (gha + lon + rs * correction))

        decimal_time = degrees(utnew) / 15
        #print(utnew, decimal_time)
        return self.__get_24_hour_local_time(decimal_time)

    def __get_range(self, value:float) -> float:
        """
        Get the range of the value.

        :param value: The domain.
        :type value: float
        :return: The resultant range.
        :rtype: float
        """
        tmp1 = value / (2.0 * pi)
        tmp2 = (2.0 * pi) * (tmp1 - int(tmp1))

        if tmp2 < 0.0:
            tmp2 += (2.0 * pi)

        return tmp2

    def __get_24_hour_local_time(self, decimal_time:float) -> datetime:
        """
        Convert the decimal time into a local time (C{datetime} object)
        and correct for a 24 hour clock.

        :param decimal_time: The decimal time.
        :type decimal_time: float
        :return: The C{datetime} objects set to either sunrise or sunset.
        :rtype: datetime
        """
        decimal_time += self.__offset_utc
        #print(decimal_time)

        if decimal_time < 0.0:
            decimal_time += 24.0
        elif decimal_time > 24.0:
            decimal_time -= 24.0

        #print(decimal_time)
        hour = int(decimal_time)
        tmp = (decimal_time - hour) * 60
        minute = int(tmp)
        tmp = (tmp - minute) * 60
        second = int(tmp)
        micro = int(round((tmp - second) * 1000000))
        return self.__date_local.replace(hour=hour, minute=minute,
                                         second=second, microsecond=micro)


def __get_rise_set(date, lat=35.9513, lon=-83.9142, zenith='official'):
    """
    The default lat and lon are for Knoxville, TN. The default zenith is
    'official'.
    """
    rs = SunriseSunset(date, lat=lat, lon=lon, zenith=zenith)
    rise_time, set_time = rs.sun_rise_set
    print(f"Using zenith: {zenith}")
    print(f"   Date/Time: {date}")
    print(f"     Sunrise: {rise_time}")
    print(f"      Sunset: {set_time}")
    print(f"    Is night: {rs.is_night()}\n")


if __name__ == '__main__':
    import sys
    import pytz
    #from pprint import pprint
    from geopy.geocoders import Nominatim
    from timezonefinder import TimezoneFinder

    ret = 1
    geolocator = Nominatim(user_agent='sunrisesunset')
    address = input('Enter an address: ')
    location = geolocator.geocode(address)
    print(location)

    if location:
        raw = location.raw
        lat = float(raw['lat'])
        lon = float(raw['lon'])
        #pprint(raw)
        text_date = input('Enter date in ISO format (yyyy-mm-dd hh:mm:ss): ')
        tf = TimezoneFinder()
        tz = tf.timezone_at(lng=lon, lat=lat)
        print(f"Timezone: {tz}")

        try:
            zone = pytz.timezone(tz)
            dt = datetime.datetime.fromisoformat(text_date)
        except pytz.UnknownTimeZoneError:
            print(f"The entered timezone '{tz}' is not valid.")
        except ValueError:
            print(f"The entered date '{text_date}' is not valid.")
        else:
            # Get sunrise and sunset for the given time and calculate
            # for all zenith types.
            dt = dt.astimezone(zone)
            # Get the zenith types.
            zenith_keys = SunriseSunset._SunriseSunset__ZENITH.keys()
            print("Test zenith")

            for zenith in zenith_keys:
                __get_rise_set(dt, lat=lat, lon=lon, zenith=zenith)

            # Get sunrise sunset for every hour of the day using the
            # default zenith.
            minutes = 20
            print(f"\nTest 24 hours for every {minutes} minutes.")

            for hour in range(24):
                # Every 20 minutes for an hour.
                for minute in range(0, 60, minutes):
                    date = dt.replace(hour=hour, minute=minute,
                                      second=0, microsecond=0)
                    __get_rise_set(date, lat=lat, lon=lon)

            ret = 0
    else:
        print(f"The address '{address}' could not be found.")

    sys.exit(ret)
