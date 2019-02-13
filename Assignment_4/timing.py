'''timing.py
A simple example of how to measure elapsed time in Python 3.3 or later.

S. Tanimoto, Feb. 8, 2019.

'''

import time

def pass_some_time_and_measure_it(n_seconds):
    # Capture the value of an internal clock, in order to
    # set a reference time.
    start_time = time.perf_counter()

    # Here you could put any computation that uses up
    # time or that waits for something.
    time.sleep(n_seconds)

    # Check the internal clock again, now that the activity
    # being timed has finished.
    end_time = time.perf_counter()

    # Compute the elapsed time:
    elapsed_time = end_time - start_time

    # In this demonstration, we print out the result.
    print("Elapsed time is: "+str(elapsed_time)+" seconds.")

# Test of this function, with n_seconds having value 5.
pass_some_time_and_measure_it(5)