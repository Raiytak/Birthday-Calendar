import datetime
from functools import lru_cache
from googletrans import Translator, constants


"""
Translates the given information into Birthdays.

The month may be given as an integer or a name
In the late case, months are translated using the google API.
"""


class TranslationError(Exception):
    """A word was impossible to translate correctly in english and should be translated manually"""

    pass


# init the Google API translator
translator = Translator()


def moveItemToPositionInList(item, index: int, list_to_modify: list):
    list_to_modify.insert(index, list_to_modify.pop(list_to_modify.index(item)))


AUTHORIZED_LANGUAGES = list(constants.LANGUAGES.keys())
# Put english in first place
moveItemToPositionInList("en", 0, AUTHORIZED_LANGUAGES)
moveItemToPositionInList("fr", 1, AUTHORIZED_LANGUAGES)


class Birthday:
    def __init__(
        self, day: int, month: str, name: str, lastname: str, identifier: str = None
    ) -> None:
        self.day = day
        self.month = month
        self.name = name
        self.lastname = lastname
        if identifier is None or identifier == "":
            identifier = self.name + " " + self.lastname
        self.identifier = identifier

    def __str__(self):
        return f"Day: '{self.day}'\nMonth: '{self.month}'\nName: '{self.name}'\nLastname: '{self.lastname}'\nIdentifier: '{self.identifier}'\n"

    @property
    def label(self):
        return f"{self.name + (' ' + self.lastname if self.lastname else '')} ({self.identifier})"

    @property
    def date(self):
        return convertStrDateIntoDatetime(self.day, self.month)

    @property
    def to_dict(self):
        return {
            self.identifier: {
                "name": self.name,
                "lastname": self.lastname,
                "birthday": {"day": self.day, "month": self.month},
            }
        }

    @property
    def to_cache(self):
        return {
            self.identifier: {
                "name": self.name,
                "lastname": self.lastname,
                "birthday": {
                    "day": self.day,
                    "month": convertStrDateIntoDatetime(self.day, self.month).month,
                },
            }
        }

    def compare_to(self, obj):
        day = "Day: " + str(self.day) + " -> " + str(obj.day)
        month = "Month: " + str(self.month) + " -> " + str(obj.month)
        name = "Name: " + self.name + " -> " + obj.name
        lastname = "Lastname: " + self.lastname + " -> " + obj.lastname
        return "\n".join([day, month, name, lastname])


def convertStrDateIntoDatetime(day, month) -> datetime.datetime:
    """The month must be fully written (the case is insensitive)
    example 1 : 
        day = '15'
        month = 'JULLY'
    example 2 : 
        day = '30'
        month = 'aoÛT'
    example 3 : 
        day = '23'
        month = '7'
    """

    if type(month) is int:
        return datetime.datetime(1900, month, day)

    @lru_cache
    def translateAndConvertIntoDatetime(day, month: str, language):
        if type(month) is str:
            translation = translator.translate(month, dest="en", src=language)
            en_month = translation.text
            return convertIntoDatetime(day, en_month)

    def convertIntoDatetime(day, en_month):
        return datetime.datetime.strptime(str(day) + " " + en_month, "%d %B")

    try:
        normalized_date = convertIntoDatetime(day, month)
        return normalized_date
    except ValueError:
        pass

    try:
        normalized_date = translateAndConvertIntoDatetime(day, month, "auto")
        return normalized_date
    except ValueError:
        pass

    i = 0
    translation_worked = False
    while not translation_worked:
        try:
            language = AUTHORIZED_LANGUAGES[i]
            normalized_date = translateAndConvertIntoDatetime(day, month, language)
            translation_worked = True
            # Put the detected language in first position to speed up the translation process
            moveItemToPositionInList(language, 0, AUTHORIZED_LANGUAGES)
            return normalized_date
        except ValueError:
            pass
            # print(f"Not working for : month: '{month}', language: '{language}'")
        except IndexError:
            raise TranslationError(
                f"The month '{month}' could not be translated in English, it should be added in english instead"
            )
        i += 1


def convertDictToBirthday(identifier, birthday_dict):
    return Birthday(
        birthday_dict["birthday"]["day"],
        birthday_dict["birthday"]["month"],
        birthday_dict["name"],
        birthday_dict["lastname"],
        identifier,
    )


def convertDictToBirthdays(data):
    birthdays = {
        identifier: convertDictToBirthday(identifier, data[identifier])
        for identifier in data.keys()
    }
    return birthdays
