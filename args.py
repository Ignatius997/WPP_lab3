import argparse
import re

_MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
_TIMES = ['mor', 'eve']

def _create_2way_mapping(names):
    return {
        key: value
        for index, name in enumerate(names, start=1)
        for key, value in ((index, name), (name, index))
    }

months_2way = _create_2way_mapping(_MONTHS)
days_2way = _create_2way_mapping(_DAYS)
times_2way = _create_2way_mapping(_TIMES)

def validate_days_range(s):
    match = re.fullmatch(r'([a-z]{3})(?:-([a-z]{3}))?', s)

    if not match:
        raise argparse.ArgumentTypeError("Expected DAY or DAY-DAY")

    x, y = match.groups()

    if x not in _DAYS or (y is not None and y not in _DAYS):
        raise argparse.ArgumentTypeError("Invalid day")

    if y is not None and _DAYS.index(x) > _DAYS.index(y):
        raise argparse.ArgumentTypeError("Start day must not follow end day")

    return s

def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--months', nargs='+', choices=_MONTHS, required=True,
                        help='Months of our interest.' +
                        'Format: three-letter abbreviation of the month, e.g. oct.')
    parser.add_argument('--days', nargs='+', required=True, type=validate_days_range,
                        help='Weekdays range of our interest. One weekdays range per month.' +
                        'Format: DAY or DAY-DAY, where DAY is a three-letter abbreviation of the weekday, e.g. tue.')
    parser.add_argument('--times', nargs='+', choices=_TIMES, required=False,
                        help='Times of day of our interest. One time of day per day.' +
                        'mor = morning, eve = evening. If not specified, mor is assumed.')

    return parser

def get_days_count(days_ranges):
    count = 0
    for day_range in days_ranges:
        if '-' in day_range:
            start_day, end_day = day_range.split('-')
            start_index = _DAYS.index(start_day)
            end_index = _DAYS.index(end_day)
            count += (end_index - start_index + 1)
        else:
            count += 1
    return count

def validate_args(args):
    if (len(args.months) != len(args.days)):
        raise argparse.ArgumentTypeError("Number of months must match number of days ranges")
    if args.times is not None and len(args.times) > get_days_count(args.days):
        raise argparse.ArgumentTypeError("Number of times must not exceed number of days ranges")

def format_args(args):
    months = [(_MONTHS.index(month) + 1) for month in args.months]
    days = []

    for day_range in args.days:
        if '-' in day_range:
            start_day, end_day = day_range.split('-')
            start_index = _DAYS.index(start_day)
            end_index = _DAYS.index(end_day)
            days.append(list(range(start_index + 1, end_index + 2)))
        else:
            days.append([_DAYS.index(day_range) + 1])

    times = [1] * get_days_count(args.days)

    if args.times is not None:
        times[:len(args.times)] = [
            1 if time == 'mor' else 2 for time in args.times
        ]

    result = []
    time_index = 0

    for month, day_list in zip(months, days):
        for day in day_list:
            result.append((month, day, times[time_index]))
            time_index += 1

    return result

def parse_arguments() -> list[tuple[int, int, int]]:
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args)
    return format_args(args)