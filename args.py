import argparse
import re

_MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
_DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

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
                        help='Months of our interest.')
    parser.add_argument('--days', nargs='+', choices=_DAYS, required=True, type=validate_days_range,
                        help='Weekdays range of our interest. One weekdays range per month.')
    parser.add_argument('--times', nargs='+', required=False,
                        help='Times of day of our interest. One time of day per day.')

    return parser

def validate_args(args):
    if (len(args.months) != len(args.days)):
        raise argparse.ArgumentTypeError("Number of months must match number of days ranges")

def parse_arguments() -> argparse.Namespace:
    parser = create_parser()
    args = parser.parse_args()
    validate_args(args)
    return args