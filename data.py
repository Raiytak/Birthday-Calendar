from pathlib import Path
import json

"""Access the data contained in 'example.json' and translate it"""

EXAMPLE_PATH = Path.cwd() / "Birthday-Calendar" / "example.json"


class BirthdayAccessor:
    def __init__(self, birthdays_path):
        if birthdays_path is None:
            birthdays_path = EXAMPLE_PATH
        self.birthdays_path = birthdays_path

    def getData(self):
        with open(self.birthdays_path, "r") as jsonfile:
            data = json.load(jsonfile)
            return data

    def addBirthday(self, entries, message_box):
        day = int(entries["Day"].get())
        message_box["text"] = f"hey I wrote {day}"

    # def check

