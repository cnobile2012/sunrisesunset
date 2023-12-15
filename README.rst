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

