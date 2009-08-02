#!/usr/bin/env python
#
# sunrisesunset.py
#
# This code is valid for dates from 1901 to 2099, and will not calculate
# sunrise/sunset times for latitudes above/below 63/-63 degrees.
#
# No external packages are used when using the class SunriseSunset. If you
# run the tests you will need to install pytz as shown below or use your
# package installer if it's available.
#
# $ sudo easy_install --upgrade pytz
#
# CVS/SVN Info
#----------------------------------
# $Author$
# $Date$
# $Revision$
#----------------------------------
##########################################################################
# Copyright (c) 2009 Carl J. Nobile.
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
#
# This Copyright covers only the implimentation of the algorithm used in
# this code and does not cover the algorithm itself which is in the
# public domain.
#
# Contributors:
#    Carl J. Nobile - initial API and implementation
##########################################################################

import datetime
from math import degrees, radians, atan, cos, sin, pi, sqrt, fabs


class SunriseSunset(object):
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

    def __init__(self, date, lat, lon, zenith='official'):
        """
        Set the values for the sunrise and sunset calculation.

        @param date: A localized datetime object that is timezone aware.
        @param lat: The latitude.
        @param lon: The longitude.
        @keyword zenith: The zenith name.
        """
        if not isinstance(date, datetime.datetime) or date.tzinfo is None:
            msg = "The date must be a datetime object with timezone info."
            raise ValueError(msg)

        if zenith not in self.__ZENITH:
            msg = "Invalid zenith name [%s] must be one of: %s"
            raise ValueError(msg % (zenith, self.__ZENITH.keys()))

        if abs(lat) > 63:
            raise ValueError('Invalid latitude: %s' % lat)

        self.__dateLocal = date
        self.__lat = lat
        self.__lon = lon
        self.__zenith = zenith
        localTuple = date.timetuple()
        utcTuple = date.utctimetuple()
        self.__offsetUTC = (localTuple[3] - utcTuple[3]) + \
                           (localTuple[4] - utcTuple[4]) / 60.0
        self.__sunrise = None
        self.__sunset = None
        self.__determineRiseSet()

    def isNight(self, collar=0):
        """
        Check if it is day or night. If the 'collar' keyword argument is
        changed it will skew the results to either before or after the real
        sunrise and sunset. This is useful if lead and lag timea are needed
        around the actual sunrise and sunset.

        Note::
            If collar == 30 then this method will say it is daytime 30
            minutes before the actual sunrise and likewise 30 minutes after
            sunset it would indicate it is night.

        @keyword collar: The minutes before or after sunrise and sunset.
        @return: True if it is night else False if day.
        """
        result = False
        delta = datetime.timedelta(minutes=collar)

        if (self.__sunrise - delta) > self.__dateLocal or \
               self.__dateLocal > (self.__sunset + delta):
            result = True

        return result

    def getSunRiseSet(self):
        """
        Get the sunrise and sunset.

        @return: A C{datetime} object in a tuple (sunrise, sunset).
        """
        return self.__sunrise, self.__sunset

    def __determineRiseSet(self):
        """
        Determine both the sunrise and sunset.
        """
        year = self.__dateLocal.year
        month = self.__dateLocal.month
        day = self.__dateLocal.day
        # Ephemeris
        ephem2000Day = 367 * year - (7 * (year + (month + 9) / 12) / 4) + \
                       (275 * month / 9) + day - 730531.5
        self.__sunrise = self.__determineRiseOrSet(ephem2000Day, 1)
        self.__sunset = self.__determineRiseOrSet(ephem2000Day, -1)

    def __determineRiseOrSet(self, ephem2000Day, rs):
        """
        Determine either the sunrise or the sunset.

        @param ephem2000Day: The Ephemeris from the beginning of the
                             21st century.
        @param rs: The factor that determines either sunrise or sunset where
                   1 equals sunrise and -1 sunset.
        @return: Either the sunrise or sunset as a C{datetime} object.
        """
        utold = pi
        utnew = 0
        altitude = self.__ZENITH[self.__zenith]
        sinAlt = sin(radians(altitude))       # solar altitude
        sinPhi = sin(radians(self.__lat))     # viewer's latitude
        cosPhi = cos(radians(self.__lat))     #
        lon = radians(self.__lon)             # viewer's longitude
        ct = 0
        #print rs, ephem2000Day, sinAlt, sinPhi, cosPhi, lon

        while fabs(utold - utnew) > 0.001 and ct < 35:
            ct += 1
            utold = utnew
            days = ephem2000Day + utold / (2 * pi)
            t = days / 36525
            # The magic numbers are orbital elements of the sun.
            l = self.__getRange(4.8949504201433 + 628.331969753199 * t)
            g = self.__getRange(6.2400408 + 628.3019501 * t)
            ec = 0.033423 * sin(g) + 0.00034907 * sin(2 * g)
            lam = l + ec
            e = -1 * ec + 0.0430398 * sin(2 * lam) - 0.00092502 * sin(4 * lam)
            obl = 0.409093 - 0.0002269 * t
            delta = sin(obl) * sin(lam)
            delta = atan(delta / sqrt(1 - delta * delta))
            gha = utold - pi + e
            cosc = (sinAlt - sinPhi * sin(delta)) / (cosPhi * cos(delta))

            if cosc > 1:
                correction = 0
            elif cosc < -1:
                correction = pi
            else:
                correction = atan((sqrt(1 - cosc * cosc)) / cosc)

            #print cosc, correction, utold, utnew
            utnew = self.__getRange(utold - (gha + lon + rs * correction))

        decimalTime = degrees(utnew) / 15
        #print utnew, decimalTime
        return self.__get24HourLocalTime(rs, decimalTime)

    def __getRange(self, value):
        """
        Get the range of the value.

        @param value: The domain.
        @return: The resultant range.
        """
        tmp1 = value / (2.0 * pi)
        tmp2 = (2.0 * pi) * (tmp1 - int(tmp1))
        if tmp2 < 0.0: tmp2 += (2.0 * pi)
        return tmp2

    def __get24HourLocalTime(self, rs, decimalTime):
        """
        Convert the decimal time into a local time (C{datetime} object)
        and correct for a 24 hour clock.

        @param rs: The factor that determines either sunrise or sunset where
                   1 equals sunrise and -1 sunset.
        @param decimalTime: The decimal time.
        @return: The C{datetime} objects set to either sunrise or sunset.
        """
        decimalTime += self.__offsetUTC
        #print decimalTime

        if decimalTime < 0.0:
            decimalTime += 24.0
        elif decimalTime > 24.0:
            decimalTime -= 24.0

        if rs == 1 and int(decimalTime) > 12:
            decimalTime -= 12
        elif rs == -1 and int(decimalTime) < 13:
            decimalTime += 12

        #print decimalTime
        hour = int(decimalTime)
        tmp = (decimalTime - hour) * 60
        minute = int(tmp)
        tmp = (tmp - minute) * 60
        second = int(tmp)
        micro = int(round((tmp - second) * 1000000))
        localDT = self.__dateLocal.replace(hour=hour, minute=minute,
                                           second=second, microsecond=micro)
        return localDT


def __getRiseSet(date, lat=35.9513, lon=-83.9142, zenith='official'):
    """
    The default lat and lon are for Knoxville, TN. The default zenith is
    'official'.
    """
    rs = SunriseSunset(date, lat, lon, zenith=zenith)
    riseTime, setTime = rs.getSunRiseSet()
    print "Using zenith: %s" % zenith
    print "Date/Time now: %s" % date
    print "Sunrise: %s" % riseTime
    print " Sunset: %s" % setTime
    print "Is night: %s\n" % rs.isNight()


if __name__ == '__main__':
    import sys, pytz
    zone = pytz.timezone("US/Eastern")

    # Get sunrise and sunset for now and all the zenith types.
    now = datetime.datetime.now(zone)
    # Get the zenith types.
    zenithKeys = SunriseSunset._SunriseSunset__ZENITH.keys()
    print "Test zenith"

    for zenith in zenithKeys:
        __getRiseSet(now, zenith=zenith)

    # Get sunrise sunset for every hour of the day using the default zenith.
    print "\nTest 24 hours"

    for hour in range(24):
        for minute in range(0, 60, 10):
            date = now.replace(hour=hour, minute=minute, second=0,
                               microsecond=0)
            __getRiseSet(date)

    sys.exit(0)
