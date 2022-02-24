from tkcalendar import Calendar

import tkinter as tk
import tkinter.filedialog


"""Create the UI elements of the application"""


class AppShell:

    FIELDS = ["Day", "Month", "Name", "Lastname", "Identifier"]

    def __init__(self):
        self.root = tk.Tk()
        self.elements = {}

        self.window = tk.Frame(self.root)
        self.elements.update({"window": self.window})
        self.elements.update(self.createCalendar(self.window))
        birthday_entries, entry_row = self.createBirthdayEntries(self.window)
        self.elements.update(entry_row)
        self.elements.update(birthday_entries)
        self.elements.update(self.createMessageBox(self.window))
        self.elements.update(self.createButtons(self.window))
        self.remove_entry = self.elements["remove_entry"]
        self.placeComponents()

    def createCalendar(self, root):
        calendar = Calendar(
            root,
            font="Arial 18",
            selectmode="day",
            disabledforeground="red",
            cursor="hand2",
        )
        calendar.tag_config("reminder", background="red", foreground="yellow")
        return {"calendar": calendar}

    def createBirthdayEntries(self, root):
        entry_row = tk.Frame(root)
        entries = {}
        for field in self.FIELDS:
            row = tk.Frame(entry_row)
            lab = tk.Label(row, width=10, text=field + ": ", anchor="w")
            ent = tk.Entry(row, width=10)
            row.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
            lab.pack(side=tk.LEFT)
            ent.pack(side=tk.LEFT)
            entries[field] = ent
        add_birthday_button = tk.Button(entry_row, text="Add Birthday")
        add_birthday_button.pack(side=tk.BOTTOM, padx=5, pady=5)
        return (
            {"birthday_entries": entries, "add_birthday_button": add_birthday_button},
            {"entry_row": entry_row},
        )

    def createMessageBox(self, root):
        message_box = tk.Frame(root)
        message_box_text = tk.StringVar(
            value="The birthdays are marked as red\nHover over or click it to see the information :)"
        )
        message_label = tk.Label(
            message_box, textvariable=message_box_text, relief=tk.RAISED
        )
        message_label.pack(side=tk.TOP, padx=5, pady=5)
        return {
            "message_box": message_box,
            "message_label": message_label,
            "message_box_text": message_box_text,
        }

    def createButtons(self, root):
        buttons = tk.Frame(root)
        upper_frame = tk.Frame(buttons)
        upper_frame.grid(row=0)
        lower_frame = tk.Frame(buttons)
        lower_frame.grid(row=1)

        remove_birthday_button = tk.Button(upper_frame, text="Remove")
        remove_birthday_button.pack(side=tk.LEFT, padx=5, pady=5)
        remove_entry = tk.Entry(upper_frame, width=10)
        remove_entry.pack(side=tk.LEFT, padx=5, pady=5)

        add_user_file_button = tk.Button(lower_frame, text="Use File")
        add_user_file_button.pack(side=tk.LEFT, padx=5, pady=5)
        quit = tk.Button(lower_frame, text="Quit", command=root.quit)
        quit.pack(side=tk.LEFT, padx=5, pady=5)

        return {
            "buttons": buttons,
            "remove_entry": remove_entry,
            "remove_birthday_button": remove_birthday_button,
            "add_user_file_button": add_user_file_button,
            "quit": quit,
        }

    def askUserFilePath(self):
        return tkinter.filedialog.askopenfilename()

    def placeComponents(self):
        self.window.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        self.elements["calendar"].grid(row=0, column=0)
        self.elements["message_box"].grid(row=1, column=0)
        self.elements["entry_row"].grid(row=0, column=1)
        self.elements["buttons"].grid(row=1, column=1)
