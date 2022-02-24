import argparse

from .accessor import BirthdayAccessor
from .convert import convertDictToBirthdays
from .app_shell import AppShell
from .app_func import AppFunctionalities

"""
Main script

Handles the arguments and craetes a mixin with the shell, core functions and accessor
"""


class MainApp(AppFunctionalities, AppShell):
    def __init__(self, birthday_accessor, birthday_convertor, *args, **kwargs):
        self.birthday_accessor = birthday_accessor
        self.birthday_convertor = birthday_convertor
        super().__init__(*args, **kwargs)

    def birthdays_data(self):
        return birthday_accessor.getData()

    def birthdays_data_from_user(self):
        if birthday_accessor.user_file:
            return birthday_accessor.getDataOfJson(birthday_accessor.user_file)
        return {}

    @property
    def birthdays(self):
        data = self.birthdays_data()
        return self.birthday_convertor(data)

    @property
    def birthdays_from_user(self):
        data = self.birthdays_data_from_user()
        return self.birthday_convertor(data)

    def saveBirthday(self, birthday):
        return self.birthday_accessor.saveBirthday(birthday)

    def saveBirthdayInCache(self, birthday):
        return self.birthday_accessor.saveBirthdayInCache(birthday)

    def deleteIdentifer(self, identifier):
        return self.birthday_accessor.removeBirthdayWithIdentifier(identifier)

    def setUserFilePath(self, path):
        self.birthday_accessor.setUserFilePath(path)

    def clearCache(self):
        self.birthday_accessor.clearCache()


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
main_app = MainApp(birthday_accessor, convertDictToBirthdays, args.years)
main_app.launchCalendar()
