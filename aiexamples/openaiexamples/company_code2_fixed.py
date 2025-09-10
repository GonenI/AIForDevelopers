import pendulum

# @@@@@@ a function to print the current date and time locally, in new york, and in london
def print_time():
    local_time = pendulum.now()
    ny_time = pendulum.now('America/New_York')
    london_time = pendulum.now('Europe/London')
    print('Local time:', local_time)
    print('New York time:', ny_time)
    print('London time:', london_time)

print_time()