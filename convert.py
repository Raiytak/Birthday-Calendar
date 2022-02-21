import datetime
from googletrans import Translator, constants


"""Translate the given information into Birthdays"""


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
    def __init__(self, day, month, surname, name, lastname=None) -> None:
        self.date = convertStrDateIntoDatetime(day, month)
        self.label = f"{name + (' ' + lastname if lastname else '')} ({surname})"


def convertStrDateIntoDatetime(day, month: str) -> datetime.datetime:
    """The month must be fully written (the case is insensitive)
    example 1 : 
        day = '15'
        month = 'JULLY'
    example 2 : 
        day = '30'
        month = 'aoÛT'
    """

    def convertIntoDatetime(day, month, language):
        translation = translator.translate(month, dest="en", src=language)
        en_month = translation.text
        return datetime.datetime.strptime(str(day) + " " + en_month, "%d %B")

    i = 0
    translation_worked = False
    while not translation_worked:
        language = AUTHORIZED_LANGUAGES[i]
        try:
            normalized_date = convertIntoDatetime(day, month, language)
            translation_worked = True
            # Put the detected language in first position to speed up the translation process
            moveItemToPositionInList(language, 0, AUTHORIZED_LANGUAGES)
        except ValueError:
            pass
            # print(f"Not working for : month: '{month}', language: '{language}'")
        except IndexError:
            raise TranslationError(
                f"The month '{month}' could not be translated in English, it should be added in english instead"
            )
        i += 1

    return normalized_date


def getBirthdaysOf(data):
    birthdays = {
        person: Birthday(
            data[person]["birthday"]["day"],
            data[person]["birthday"]["month"],
            person,
            data[person]["name"],
            data[person]["lastname"] or None,
        )
        for person in data.keys()
    }
    return birthdays
