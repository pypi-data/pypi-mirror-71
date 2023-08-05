# PPT - The Python Performance Tuner

`ppt` is a tool for tuning the performance of Python programs.

## Install

~~~shell
pip install ppt
~~~

## Example

### Timing

~~~python
import ppt
import time

if __name__ == '__main__':

    for _ in range(10):

        ppt.time('big')
        time.sleep(0.5)  # Big computation

        ppt.time('medium')
        time.sleep(0.3)  # Medium computation

        ppt.time('fast')
        time.sleep(0.01)  # Fast computation

    # Stop current timing
    ppt.stop()

    # Print current timings
    ppt.summary()

    # Detailed statistics from pstats
    ppt.stats()

~~~

**Output**

~~~
big: 40 function calls in 5.006 seconds
medium: 40 function calls in 3.003 seconds
fast: 40 function calls in 0.101 seconds
********** big **********
         40 function calls in 5.006 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       10    5.005    0.501    5.005    0.501 {built-in method time.sleep}
       10    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:42(time)
       10    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:17(stop)
       10    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


********** medium **********
         40 function calls in 3.003 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       10    3.003    0.300    3.003    0.300 {built-in method time.sleep}
       10    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:42(time)
       10    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:17(stop)
       10    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}


********** fast **********
         40 function calls in 0.101 seconds

   Ordered by: cumulative time

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
       10    0.101    0.010    0.101    0.010 {built-in method time.sleep}
        9    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:42(time)
       10    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:17(stop)
        1    0.000    0.000    0.000    0.000 /home/seba-1511/Dropbox/Dev/perf/ppt/profiler.py:53(stop)
       10    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
~~~

### Plotting

The following start a Visdom server and plots 4 lines of random samples.

~~~python
import ppt
import random, time

if __name__ == '__main__':
    ppt.plot(1)
    ppt.plot(1)
    ppt.plot(1)
    ppt.plot(1)
    for i in range(10):
        for session in ['a', 'b', 'c', 'd']:
            time.sleep(0.2)
            ppt.plot(random.random(), session)
    ppt.close()
~~~
