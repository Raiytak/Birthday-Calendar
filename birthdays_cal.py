from tkcalendar import Calendar
import datetime

try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk

"""Generate the calendar and mark the desired dates"""

DEFAULT_DELTA = 1
FIELDS = ["Day", "Name", "Lastname", "Surname"]


# Segment of years centered around today's year and within DELTA
def generateSegmentOfYears(delta):
    if delta is None:
        delta = DEFAULT_DELTA
    return [
        datetime.datetime.today().year + year_delta
        for year_delta in range(-delta, delta, 1)
    ]


def addBirthdaysForYear(calendar, birthdays: dict, year: int):
    for person_birthday in birthdays.values():
        person_birthday_date = person_birthday.date.replace(year=year)
        calendar.calevent_create(
            person_birthday_date, person_birthday.label, "reminder"
        )


def addBirthdayDates(tkinter_box, birthdays, years):
    calendar = Calendar(
        tkinter_box,
        font="Arial 14",
        selectmode="day",
        disabledforeground="red",
        cursor="hand2",
    )

    for year in generateSegmentOfYears(years):
        addBirthdaysForYear(calendar, birthdays, year)

    calendar.tag_config("reminder", background="red", foreground="yellow")
    calendar.pack(fill="both", expand=True)
    ttk.Label(
        tkinter_box, text="The birthdays are marked as red, hover over it :)"
    ).pack()

    return tkinter_box


def newBirthdayEntries(tkinter_box):
    entries = {}
    for field in FIELDS:
        row = tk.Frame(tkinter_box)
        lab = tk.Label(row, width=10, text=field + ": ", anchor="w")
        ent = tk.Entry(row, width=10)
        if field == "Day":
            ent.insert(0, "1")
        else:
            ent.insert(0, "")
        row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.LEFT)
        entries[field] = ent
    return entries


def launchCalendar(birthdays, years, birthday_accessor):
    tkinter_box = tk.Tk()

    addBirthdayDates(tkinter_box, birthdays, years)

    entries = newBirthdayEntries(tkinter_box)
    tkinter_box.bind("<Return>", (lambda event, e=entries: fetch(e)))

    message_box = tk.Label(tkinter_box)
    message_box.pack(side=tk.LEFT, padx=5, pady=5)

    add_birthday = tk.Button(
        tkinter_box,
        text="Add Birthday",
        command=(lambda e=entries: birthday_accessor.addBirthday(e, message_box)),
    )
    add_birthday.pack(side=tk.LEFT, padx=5, pady=5)

    quit = tk.Button(tkinter_box, text="Quit", command=tkinter_box.quit)
    quit.pack(side=tk.LEFT, padx=5, pady=5)

    tkinter_box.mainloop()
