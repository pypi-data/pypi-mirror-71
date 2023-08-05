================
**anothertimer**
================
Repository: https://github.com/dangcpham/anothertimer

Just another timer for code timing. anothertimer enables easy timing for code runs, saving timing data, and provides basic plotting capabilities. Example usage:
::

   from anothertimer import Timer
   timer = Timer()
   timer.tic()
   #some code here
   timer.toc()

Saving and loading data (modes 'a' for append and 'w' for write):
::

   timer.dump('example.csv', mode='a')
   timer.load('example2.csv')

Plotting can be done via:
::

   timer.plot()

Check out example.py on GitHub for some more features (stopwatch/sections) and plots!

Installation
============

:: 

   pip install anothertimer

Dependecies
===========
1. Standard Python libraries (typing, time, os, csv).
2. matplotlib (optional) - for plotting.

Overhead
========
Measured by pstats on example.py, core functionalities causes minimal (<0.001s) 
overhead. Plotting causes some overhead (due to matplotlib plotting, on the 
order of a few seconds), so plot carefully.


Precision
=========

Currently, anothertimer uses the time.time() function to keep track of time. The precision is in the sub-second range (read more about Python timing at https://www.python.org/dev/peps/pep-0564/,  https://stackoverflow.com/questions/1938048/high-precision-clock-in-python). Currently, it is not a good idea to use this package for high precision applications, consider the timeit module.
