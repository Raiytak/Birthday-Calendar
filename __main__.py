import argparse

from accessor import BirthdayAccessor
from convert import convertDictToBirthdays
from app_shell import AppShell
from app_func import AppFunctionalities


class MainApp(AppFunctionalities, AppShell):
    def __init__(self, birthday_accessor, birthday_convertor, *args, **kwargs):
        self.birthday_accessor = birthday_accessor
        self.birthday_convertor = birthday_convertor
        super().__init__(*args, **kwargs)

    def birthdays_data(self):
        return birthday_accessor.getData()

    @property
    def birthdays(self):
        data = self.birthdays_data()
        return self.birthday_convertor(data)

    def saveBirthday(self, birthday):
        return self.birthday_accessor.saveBirthday(birthday)

    def deleteIdentifer(self, identifier):
        return self.birthday_accessor.removeBirthdayWithIdentifier(identifier)


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
parser.add_argument(
    "--user-file-path",
    nargs=argparse.OPTIONAL,
    const=True,
    help="Option to pop up a window that asks the user for its file path",
)
args = parser.parse_args()

if args.user_file_path is None:
    path = args.path
else:
    path = None
birthday_accessor = BirthdayAccessor(path)

main_app = MainApp(birthday_accessor, convertDictToBirthdays, args.years)
main_app.launchCalendar()
