import os
from pathlib import Path
import json

"""Access the data contained in 'example.json' and translate it"""

HOME = Path.home()
APP_FOLDER = ".birthday_calendar"
NORMALIZED_JSON = "normalized.json"


class BirthdayAccessor:
    def __init__(self, user_file):
        self.folder = HOME / APP_FOLDER
        self.cache = self.folder / NORMALIZED_JSON
        self.user_file = user_file
        self.initAppFolder()

    def initAppFolder(self):
        if not Path.exists(self.folder):
            os.mkdir(self.folder)
        if Path.exists(self.folder / NORMALIZED_JSON):
            try:
                self.getDataOfJson(self.folder / NORMALIZED_JSON)
            except json.decoder.JSONDecodeError:
                os.remove(self.folder / NORMALIZED_JSON)
        if not Path.exists(self.folder / NORMALIZED_JSON):
            with open(self.folder / NORMALIZED_JSON, "w", encoding="utf-8") as jsonfile:
                json.dump({}, jsonfile, indent=4)

    def getDataOfJson(self, path):
        with open(path, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            return data

    def getData(self):
        return self.getDataOfJson(self.cache)

    def identifierExists(self, identifier):
        data = self.getDataOfJson(self.cache)()
        return identifier in data.keys()

    def saveBirthdayUsingConversionIn(self, birthday, conversion, json_path):
        updated_birthday = None
        data = self.getDataOfJson(json_path)
        with open(json_path, "w", encoding="utf-8") as file:
            identifier = birthday.identifier
            if identifier in data.keys():
                updated_birthday = birthday
                del data[identifier]
            data.update(getattr(birthday, conversion))
            json.dump(data, file, indent=4)
        return updated_birthday

    def saveBirthdayInCache(self, birthday):
        return self.saveBirthdayUsingConversionIn(birthday, "to_cache", self.cache)

    def saveBirthdayInUser(self, birthday):
        if self.user_file:
            return self.saveBirthdayUsingConversionIn(
                birthday, "to_dict", self.user_file
            )
        return None

    def saveBirthday(self, birthday):
        updated_birthday = self.saveBirthdayInCache(birthday)
        updated_birthday_from_user = self.saveBirthdayInUser(birthday)
        return updated_birthday

    def removeBirthdayWithIdentifierIn(self, identifier: str, path):
        data = self.getDataOfJson(path)
        with open(path, "w", encoding="utf-8") as file:
            del data[identifier]
            json.dump(data, file, indent=4)

    def removeBirthdayWithIdentifierFromCache(self, identifier: str):
        self.removeBirthdayWithIdentifierIn(identifier, self.cache)

    def removeBirthdayWithIdentifierFromUser(self, identifier: str):
        if self.user_file:
            self.removeBirthdayWithIdentifierIn(identifier, self.user_file)

    def removeBirthdayWithIdentifier(self, identifier: str):
        self.removeBirthdayWithIdentifierFromCache(identifier)
        self.removeBirthdayWithIdentifierFromUser(identifier)
