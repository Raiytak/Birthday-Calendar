import datetime

from .convert import Birthday

"""Core functionalities of the application"""


class AppFunctionalities:

    YEARS_DELTA = 1

    def __init__(self, delta, *args, **kwargs):
        self.events = {}
        if delta is None:
            delta = AppFunctionalities.YEARS_DELTA
        self.delta = delta
        super().__init__(*args, **kwargs)
        self.addBirthdaysToCalendar(self.elements["calendar"], self.birthdays)
        self.elements["add_birthday_button"].configure(
            command=lambda entries=self.elements["birthday_entries"]: self.addBirthday(
                entries
            )
        )

        # Binding of events
        # self.root.bind(
        #     "<Return>", (lambda event, e=self.elements["birthday_entries"]: fetch(e))
        # )
        self.elements["remove_birthday_button"].configure(
            command=lambda remove_entry=self.elements[
                "remove_entry"
            ]: self.removeIdentifier(remove_entry)
        )
        self.elements["add_user_file_button"].configure(command=self.useUserFile)
        self.elements["calendar"].bind("<<CalendarSelected>>", self.showSelectionToUser)

    # Segment of years centered around today's year and within DELTA
    def generateSegmentOfYears(self, delta: int):
        if delta is None:
            delta = self.years
        elif delta < 1:
            delta = 1
        return [
            datetime.datetime.today().year + year_delta
            for year_delta in range(-delta, delta + 1, 1)
        ]

    def addBirthdaysToCalendar(self, calendar, birthdays):
        for birthday in birthdays.values():
            self.createCalendarEvent(calendar, birthday)

    def addBirthdaysToCalendarAndSaveInCache(self, calendar, birthdays):
        for birthday in birthdays.values():
            self.saveBirthdayInCache(birthday)
            self.createCalendarEvent(calendar, birthday)

    def createCalendarEvent(self, calendar, birthday):
        for year in self.generateSegmentOfYears(self.delta):
            person_birthday_date = birthday.date.replace(year=year)
            event_id = calendar.calevent_create(
                person_birthday_date, birthday.label, "reminder"
            )
            if birthday.identifier not in self.events.keys():
                self.events[birthday.identifier] = []
            self.events[birthday.identifier].append(event_id)

    def deleteCalendarBirthday(self, calendar, birthday):
        self.deleteCalendarEventWithIdentifier(calendar, birthday.identifier)

    def deleteCalendarEventWithIdentifier(self, calendar, identifier):
        for event_id in self.events[identifier]:
            calendar.calevent_remove(event_id)

    def deleteAllBirthdays(self):
        self.elements["calendar"].calevent_remove("all")
        self.clearCache()

    def useUserFile(self):
        path = self.askUserFilePath()
        self.setUserFilePath(path)
        self.deleteAllBirthdays()
        birthdays = self.birthdays_from_user
        self.addBirthdaysToCalendarAndSaveInCache(self.elements["calendar"], birthdays)

    def addBirthday(self, entries):
        ENTRIES_CHECK_AND_ADD = ["Name", "Lastname"]
        for entry in entries.keys():
            if entries[entry].get() is None:
                self.showMessage(f"No {entry} was provided")
        birthday_inputs = []
        day = entries["Day"].get()
        if not day.isdigit():
            self.showMessage(f"The day provided should be an int, but is '{day}'")
            return
        day = int(day)
        if day > 31 or day < 1:
            self.showMessage(
                f"The day provided should be between 31 and 1, but is '{day}'"
            )
            return
        birthday_inputs.append(day)

        month = entries["Month"].get()
        if month.isdigit():
            month = int(month)
            if month > 12 or month < 1:
                self.showMessage(
                    f"The month provided should be a name or a number comprised between 12 and 1, but is '{month}'"
                )
                return
            birthday_inputs.append(month)
        else:
            ENTRIES_CHECK_AND_ADD.insert(0, "Month")

        for entry in ENTRIES_CHECK_AND_ADD:
            value = entries[entry].get()
            if value == "":
                self.showMessage(f"The value of '{entry}' is empty")
                return
            birthday_inputs.append(value)
        birthday_inputs.append(entries["Identifier"].get())

        new_birthday = Birthday(*birthday_inputs)
        updated_birthday = self.saveBirthday(new_birthday)
        if updated_birthday is None:
            self.showMessage("Birthday added:\n" + str(new_birthday))
        else:
            identifier = updated_birthday.identifier
            self.showMessage(
                f"Birthday with identifier '{identifier}' was updated:\n"
                + updated_birthday.compare_to(new_birthday)
            )
            self.deleteCalendarBirthday(self.elements["calendar"], new_birthday)

        self.createCalendarEvent(self.elements["calendar"], new_birthday)

    def removeIdentifier(self, remove_entry):
        data = self.birthdays_data()
        identifier = remove_entry.get()
        if not identifier in data.keys():
            self.showMessage(
                f"The identifier '{identifier}' was not found in the birthday list"
            )
        else:
            self.deleteCalendarEventWithIdentifier(
                self.elements["calendar"], identifier
            )
            self.deleteIdentifer(identifier)
            self.showMessage(f"The identifier '{identifier}' has been removed")

    def showSelectionToUser(self, entry):
        selected_date = self.elements["calendar"].selection_get()
        events_id = self.elements["calendar"].get_calevents(selected_date)
        if events_id:
            message = f"{selected_date} has the birthdays of:\n" + "\n".join(
                [
                    self.elements["calendar"].calevent_cget(id, "text")
                    for id in events_id
                ]
            )
            self.showMessage(message)

    def showMessage(self, message):
        self.elements["message_box_text"].set(message)

    def launchCalendar(self):
        self.root.mainloop()
