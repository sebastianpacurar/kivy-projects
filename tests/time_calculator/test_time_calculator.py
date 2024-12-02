import pytest

from projects.time_calculator.screen import TimeCalculatorScreen


@pytest.fixture
def screen():
    """ Initialize Test Screen """
    return TimeCalculatorScreen()


@pytest.fixture(
    params=[12, 24, 48],
    ids=["12h initial", "24h initial", "48h initial"]
)
def initial_time(request):
    return request.param * 3600  # convert hours to seconds


@pytest.fixture(
    params=[(0, 0),  # Minimum values
            (0, 59),  # Max seconds without rollover
            (59, 59),  # Max minutes and seconds
            (60, 0),  # Exactly 1 hour in minutes
            (59, 60),  # Rollover into the next hour
            (60, 59),  # Almost 2 hours
            (0, 60),  # Rollover from seconds to minutes
            (59, 119),  # Multi-rollover (119 seconds = 1 min 59 sec)
            (0, 3600),  # 1 hour in seconds
            (120, 0),  # Exactly 2 hours in minutes
            (0, 7200),  # 2 hours in seconds
            (60, 60),  # Rollover with max values
            (1000, 0),  # Large number of minutes
            (0, 86400),  # A full day in seconds
            ],
    ids=["(0, 0)|zero_time",
         "(0, 59)|max_seconds",
         "(59, 59)|max_minutes_seconds",
         "(60, 0)|one_hour",
         "(59, 60)|rollover_to_next_hour",
         "(60, 59)|almost_two_hours",
         "(0, 60)|sixty_seconds",
         "(59, 119)|multi_rollover_seconds",
         "(0, 3600)|one_hour_seconds",
         "(120, 0)|two_hours_minutes",
         "(0, 7200)|two_hours_seconds",
         "(60, 60)|max_values_rollover",
         "(1000, 0)|large_minutes",
         "(0, 86400)|full_day_seconds",
         ]
)
def time_input(request):
    return request.param


def test_add_minutes_and_seconds(screen, initial_time, time_input):
    """
    Verify adding minutes and seconds to the timer using the provided time_input returns correct output.

    Steps:
    1. Set the initial time on the screen by adding initial_time (from fixture).
    2. Add the time_input (minutes and seconds) to the screen's current time.
    3. Calculate the expected time after addition.
    4. Verify that the screen's time matches the expected time.

    Example:
        - If the input is (minutes=65, seconds=75), the expected result is 1 hour 6 minutes and 15 seconds added to the screen's initial time.
    """
    minutes, seconds = time_input

    # set the initial time (ex: 12 hours, 24 hours, 48 hours)
    screen.add_minutes_and_seconds(initial_time // 60, 0)  # Convert seconds to minutes for add function

    # add the time_input (minutes and seconds)
    screen.add_minutes_and_seconds(minutes, seconds)

    # calculate expected time after addition
    expected_hours, expected_minutes, expected_seconds = calculate_expected_time_after_add(minutes, seconds, initial_time)

    assert screen.timer['hours'] == expected_hours
    assert screen.timer['minutes'] == expected_minutes
    assert screen.timer['seconds'] == expected_seconds

    print(f"\n {minutes} minutes, {seconds} seconds\n"
          f"Expected: {expected_hours} hours, {expected_minutes} minutes, {expected_seconds} seconds\n")


def test_subtract_minutes_and_seconds(screen, initial_time, time_input):
    """
    Verify subtracting minutes and seconds from the timer using the provided time_input returns correct output.

    Steps:
    1. Set the initial time on the screen by adding the initial_time.
    2. Subtract the time_input (minutes and seconds) from the screen's time.
    3. Calculate the final time after subtraction.
    4. Verify that the screen's time matches the expected result after subtraction.

    Example:
        - If the initial time is 10 hours and we subtract 5 minutes and 30 seconds,
          the expected result is 9 hours, 54 minutes, and 30 seconds.
    """
    minutes, seconds = time_input

    # add the initial time (ex: 12 hours, 24 hours, 48 hours)
    screen.add_minutes_and_seconds(initial_time // 60, 0)  # convert seconds to minutes for add function

    # subtract the time_input (minutes and seconds)
    screen.subtract_minutes_and_seconds(minutes, seconds)  # subtract the time from the screen

    # calculate the total time after subtraction
    initial_total_seconds = initial_time  # initial time in seconds
    time_to_subtract_seconds = (minutes * 60) + seconds  # time to subtract in seconds

    # final time after subtraction
    final_total_seconds = initial_total_seconds - time_to_subtract_seconds

    # ensure only values >= 0 are allowed
    final_total_seconds = max(final_total_seconds, 0)

    # calculate expected values based on the subtraction
    expected_hours = final_total_seconds // 3600
    expected_minutes = (final_total_seconds % 3600) // 60
    expected_seconds = final_total_seconds % 60

    assert screen.timer['hours'] == expected_hours
    assert screen.timer['minutes'] == expected_minutes
    assert screen.timer['seconds'] == expected_seconds

    print(f"\nInitial Time -> {initial_time // 3600} hours\n"
          f"Subtracted: {minutes} minutes, {seconds} seconds\n"
          f"Expected: {expected_hours} hours, {expected_minutes} minutes, {expected_seconds} seconds\n"
          f"Result: {screen.timer['hours']} hours, {screen.timer['minutes']} minutes, {screen.timer['seconds']} seconds\n")


def calculate_expected_time_after_add(minutes, seconds, initial_time_in_sec):
    """ Helper function to calculate expected hours, minutes, and seconds based on total time in seconds """
    total_seconds = initial_time_in_sec + (minutes * 60) + seconds

    # calculate hours, minutes, and seconds
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return hours, minutes, seconds
