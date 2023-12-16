**************
Sunrise Sunset
**************

.. image:: https://img.shields.io/pypi/v/sunrisesunset.svg
   :target: https://pypi.python.org/pypi/sunrisesunset
   :alt: PyPi Version

.. image:: http://img.shields.io/pypi/wheel/sunrisesunset.svg
   :target: https://pypi.python.org/pypi/sunrisesunset
   :alt: PyPI Wheel

.. image:: http://img.shields.io/pypi/pyversions/sunrisesunset.svg
   :target: https://pypi.python.org/pypi/sunrisesunset
   :alt: Python Versions

.. image:: http://img.shields.io/pypi/l/sunrisesunset.svg
   :target: https://pypi.python.org/pypi/sunrisesunset
   :alt: License

The MIT License (MIT)

Overview
========

Python API to determine sunrise and sunset. It accepts five zenths: official
civil, nautical, amateur, and astronomical.

Basic Usage
===========

.. code-block:: python

    import datetime
    from sunrisesunset import SunriseSunset

    dt = datetime.datetime.now()    
    rs = SunriseSunset(dt, lat=35.9513, lon=83.9142, zenith='official')
    rise_time, set_time = rs.sun_rise_set
    print(f"     Sunrise: {rise_time}")
    print(f"      Sunset: {set_time}")
    print(f"    Is night: {rs.is_night()}\n")

Running the Test
================

The pip installed package will not be enough to run the test. You will
also need to pip install geopy and timezonefinder.

There is a more complete example in the test at the end of the
```sunrisesunset.py``` file.

You will be asked for an address, just a city name is okay. Then you will
be asked for the time. It takes an ISO formatted time at minimum the year,
month, and day needs to be entered.

.. code-block:: console

    python sunrisesunset/sunrisesunset.py

    Enter an address: Chicago
    Chicago, Cook County, Illinois, United States
    Enter date in ISO format (yyyy-mm-dd hh:mm:ss): 2023-12-16 12
    Timezone: America/Chicago
    Test zenith
    Using zenith: official
       Date/Time: 2023-12-16 12:00:00-05:00
         Sunrise: 2023-12-16 08:11:12.111139-05:00
          Sunset: 2023-12-16 17:20:16.524534-05:00
        Is night: False

    Using zenith: civil
       Date/Time: 2023-12-16 12:00:00-05:00
         Sunrise: 2023-12-16 07:39:33.419425-05:00
          Sunset: 2023-12-16 17:51:55.167217-05:00
        Is night: False

    Using zenith: nautical
       Date/Time: 2023-12-16 12:00:00-05:00
         Sunrise: 2023-12-16 07:04:25.491129-05:00
          Sunset: 2023-12-16 18:27:03.015662-05:00
        Is night: False

    Using zenith: amateur
       Date/Time: 2023-12-16 12:00:00-05:00
         Sunrise: 2023-12-16 06:47:20.286033-05:00
          Sunset: 2023-12-16 18:44:08.169022-05:00
        Is night: False

    Using zenith: astronomical
       Date/Time: 2023-12-16 12:00:00-05:00
         Sunrise: 2023-12-16 06:30:29.951023-05:00
          Sunset: 2023-12-16 19:00:39.782789-05:00
        Is night: False

    Test 24 hours
    ...
