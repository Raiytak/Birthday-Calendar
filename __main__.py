import argparse

from birthdays_cal import launchCalendar
from data import BirthdayAccessor
from convert import getBirthdaysOf


parser = argparse.ArgumentParser()
parser.add_argument(
    "-p",
    "--path",
    help="Path to the json containing the information on the birthdays' person name and date",
    type=str,
)
parser.add_argument(
    "-y",
    "--years",
    help="Number of years around today's year on which the birthdays are added to the calendar (minimum 1)",
    type=int,
)
args = parser.parse_args()

birthday_accessor = BirthdayAccessor(args.path)
data = birthday_accessor.getData()
birthdays = getBirthdaysOf(data)
launchCalendar(birthdays, args.years, birthday_accessor)
