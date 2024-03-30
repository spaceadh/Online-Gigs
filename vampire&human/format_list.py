#!/usr/bin/env python3
"""Format a list of items so that they are comma separated and "and" appears before the last item.
   Vampire Hunting v1.4.0
"""

# This function will convert a "day" and a "AM/PM" Boolean to a "time"
# where time is True for AM and False for PM
def time_of_day(d,b):
    if d == 0:
        return 0 # AM/PM doesn't matter for initial period
    return ((2 * d) - (1 if b else 0))

# This function will convert a "time" to a "day"
def day_of_time(n):
    return ((n + 1) // 2)

# This function will convert a "time" to an AM/PM Boolean
def period_of_time(n):
    if n == 0:
        return True
    return ((n + 1) % 2 == 0)

# Checks whether a given "time" is the initial period
def is_initial(n):
    return n == 0

# This function turns a "time" into a day/am-pm string
def str_time(t):
    if is_initial(t):
        return "0"
    return f'{day_of_time(t)} ({"AM" if period_of_time(t) else "PM"})'

def format_list(data):
    """Format a list of items so that they are comma separated and "and"
    appears before the last item.

    Args:
        data (list): the list of items to format

    Returns:
        str: A string containing the items from data with nice formatting
    """
    # Handle the case where the list is empty
    if len(data) == 0:
        return "(None)"

    # Start with an empty string that we will add items to
    retval = ""

    sorted_data = sorted(data)
    # Handle all of the items except for the last two
    for i in range(0, len(sorted_data) - 2):
        retval = retval + str(sorted_data[i]) + ", "

    # Handle the second last item
    if len(sorted_data) >= 2:
        retval += str(sorted_data[-2]) + " and "

    # Handle the last item
    retval += str(sorted_data[-1])

    # Return the result
    return retval

def format_list_or(data):
    """Format a list of items so that they are comma separated and "and"
    appears before the last item.

    Args:
        data (list): the list of items to format

    Returns:
        str: A string containing the items from data with nice formatting
    """
    # Handle the case where the list is empty
    if len(data) == 0:
        return "(None)"

    # Start with an empty string that we will add items to
    retval = ""

    sorted_data = sorted(data)
    # Handle all of the items except for the last two
    for i in range(0, len(sorted_data) - 2):
        retval = retval + str(sorted_data[i]) + ", "

    # Handle the second last item
    if len(sorted_data) >= 2:
        retval += str(sorted_data[-2]) + " or "

    # Handle the last item
    retval += str(sorted_data[-1])

    # Return the result
    return retval

# Run some tests if the module has not been imported
if __name__ == "__main__":
    # Test the empty list
    values = []

    print(values, "is formatted as", format_list(values))

    # Test a list containing a single item
    values = [1]
    print(values, "is formatted as", format_list(values))

    # Test a list containing two items
    values = [3, 4]
    print(values, "is formatted as", format_list(values))

    # Test a list containing three items
    values = [-1, -2, -3]
    print(values, "is formatted as", format_list(values))

    # Test a list containing four items
    values = ["Alice", "Bob", "Chad", "Diane"]
    print(values, "is formatted as", format_list(values))

    # Test a list containing lots of items
    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 9]
    print(values, "is formatted as", format_list(values))

    # Test the various time functions.
    for i in range(0,10):
        p = period_of_time(i)
        d = day_of_time(i)
        i2 = time_of_day(d,p)
        s = str_time(i)
        t = "\t" if i == 0 else ""
        print(f'i:{i}\td:{d}\tp:{p}\ti2:{i2}\ts:"{s}"{t}\tok:{i == i2}')
