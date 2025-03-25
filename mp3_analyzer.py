import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from pathlib import Path
from mutagen.mp3 import MP3
import matplotlib.pyplot as plt
import datetime

# create window
root = tk.Tk()
root.title("mp3 analyzer")

# # UNIVERSAL FUNCTIONS


# convert 01:02:03 to 3723.0
def tts(time):
    return sum(float(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))


# convert 3723.0 to 01:02:03
def stt(seconds):
    return str(datetime.timedelta(seconds=seconds))


# add each file to an array as an mp3 object (will this be super slow? who give a shit)
def mp3Array(path, library):
    dbProgress.start()
    for i in Path(path).glob("**/*.mp3"):
        library.append(MP3(i))
        dbProgress.step(100 / len(list(Path(path).glob("**/*.mp3"))))
        root.update_idletasks()
    dbProgress.stop()
    initialize.pack_forget()
    theReal(library)


# open a directory and then initialize the mp3 array
def open():
    path = filedialog.askdirectory()
    library = []
    mp3Array(path, library)


# # USER OPTION FUNCTIONS


# general menu options
def generalOptions(library, var, text, input):
    match var.get():
        case 0:
            text["text"] = (
                f"the total length of all songs in your library is {stt(totalLength(library))}"
            )
        case 1:
            text["text"] = (
                f"the average length of all songs in your library is {stt(average(library))}"
            )
        case 2:
            text["text"] = "histogram opened"
            lengthHistogram(library)
        case 3:
            text["text"] = (
                f"the average length of all albums in your library is {stt(averageAlbumLength(library))}"
            )
        case 4:
            text["text"] = (
                f"the average track count of all albums in your library is {averageAlbumTrackCount(library)}"
            )
        case _:
            text["text"] = "invalid input. dumb fuck"


# album menu options
def albumOptions(library, var, text, input):
    subLibrary = []
    for i in library:
        if str(i.get("TALB")).lower() == input.lower():
            subLibrary.append(i)

    # if no text is input, notify and exit the function
    if input == "":
        text["text"] = f"please enter an album in the box at the top"
        return
    # if no album matches that name, notify and exit the function
    if len(subLibrary) == 0:
        text["text"] = f"album not found! try again"
        return

    match var.get():
        case 0:
            text["text"] = (
                f"the total length of all songs in {input} is {stt(totalLength(subLibrary))}"
            )
        case 1:
            text["text"] = (
                f"the average length of all songs in {input} is {stt(average(subLibrary))}"
            )
        case 2:
            text["text"] = f"histogram opened"
            lengthHistogram(subLibrary)
        case _:
            text["text"] = f"invalid input. dumb fuck"


# artist menu options
def artistOptions(library, var, text, input):
    subLibrary = []
    for i in library:
        if str(i.get("TPE1")).lower() == input.lower():
            subLibrary.append(i)

    # if no text is input, notify and exit the function
    if input == "":
        text["text"] = f"please enter an artist name in the box at the top"
        return
    # if no artist matches that name, notify and exit the function
    if len(subLibrary) == 0:
        text["text"] = f"artist not found! try again"
        return

    match var.get():
        case 0:
            text["text"] = (
                f"the total length of all songs by {input} is {stt(totalLength(subLibrary))}"
            )
        case 1:
            text["text"] = (
                f"the average length of all songs by {input} is {stt(average(subLibrary))}"
            )
        case 2:
            text["text"] = f"histogram opened"
            lengthHistogram(subLibrary)
        case 3:
            text["text"] = (
                f"the average length of all albums by {input} is {stt(averageAlbumLength(subLibrary))}"
            )
        case 4:
            text["text"] = (
                f"the average track count of all albums by {input} is {averageAlbumTrackCount(subLibrary)}"
            )
        case _:
            text["text"] = f"invalid input. dumb fuck"


# year menu options
def yearOptions(library, var, text, input):
    match var.get():
        case 0:
            text["text"] = (
                f"the average release year of a song is {averageYear(library)}"
            )
        case 1:
            text["text"] = "histogram opened"
            yearHistogram(library)
        case _:
            text["text"] = "invalid input. dumb fuck"


# # STUFF FUNCTIONS


# total song length
def totalLength(library):
    return sum([i.info.length for i in library])


# average
def average(library):
    return totalLength(library) / len(library)


# length histogram
def lengthHistogram(library):
    plt.hist([i.info.length for i in library])
    plt.show()


# average album length
def averageAlbumLength(library):
    lengths = []
    length = 0
    title = library[0].get("TALB")
    for i in library:
        if i.get("TALB") == title:
            length += i.info.length
        else:
            lengths.append(length)
            title = i.get("TALB")
            length = i.info.length
    lengths.append(length)

    return sum(lengths) / len(lengths)


# average album track count
def averageAlbumTrackCount(library):
    trackCounts = []
    trackCount = 0
    title = library[0].get("TALB")
    for i in library:
        if i.get("TALB") == title:
            trackCount += 1
        else:
            trackCounts.append(trackCount)
            title = i.get("TALB")
            trackCount = 1
    trackCounts.append(trackCount)

    return sum(trackCounts) / len(trackCounts)


# average year
def averageYear(library):
    list = []
    for i in library:
        if int(str(i.get("TRCK"))) == 1:
            list.append(int(str(i.get("TDRC"))))
    return sum(list) / len(list)


# histogram of years
def yearHistogram(library):
    plt.hist([int(str(i.get("TDRC"))) for i in library])
    plt.show()


# # TKINTER STUFF


# add a new page to the notebook
def makePage(master, library, tabText, titleText, entryBool, values, function):
    general = ttk.Frame(master)
    master.add(general, text=tabText)

    wrapper = tk.Frame(general, padx=50, pady=10)

    # page title (includes entry box)
    titleFrame = tk.Frame(wrapper)
    title = tk.Label(titleFrame, text=titleText)
    title.grid(row=1, column=1)

    entry = tk.Entry(titleFrame)
    if entryBool == True:
        entry.grid(row=1, column=2)

    # radio buttons for options
    optionsFrame = tk.Frame(wrapper, relief=tk.RAISED, borderwidth="5")
    var = tk.IntVar(optionsFrame)
    for i, x in enumerate(values):
        tk.Radiobutton(optionsFrame, text=x, variable=var, value=i).grid(
            row=i, sticky="w"
        )
    optionsFrame.columnconfigure(0, minsize=200, weight=1)

    # enter button to run selected option
    enter = tk.Button(
        wrapper,
        text="enter",
        command=lambda: function(library, var, text, input=entry.get()),
    )

    # text to display information
    text = tk.Label(
        wrapper,
        text="select an option and press the enter button, or switch to a different tab for more options",
        wraplength=300,
        justify=tk.LEFT,
    )

    titleFrame.grid(row=0, pady=10)
    optionsFrame.grid(row=2, pady=10)
    enter.grid(row=3, pady=5)
    text.grid(row=4, pady=10)

    wrapper.pack()


# the main program itself
def theReal(library):
    notebook = ttk.Notebook(root)
    notebook.pack(expand=1, fill=tk.BOTH)

    # general page
    generalValues = [
        "total length",
        "average song length",
        "histogram of song lengths",
        "average album length",
        "average album track count",
    ]
    makePage(
        notebook,
        library,
        "general",
        "options for all songs",
        False,
        generalValues,
        generalOptions,
    )

    # album page
    albumValues = [
        "total length",
        "average song length",
        "histogram of song lengths",
    ]
    makePage(
        notebook,
        library,
        "album",
        "options for a specific album:",
        True,
        albumValues,
        albumOptions,
    )

    # artist page
    artistValues = [
        "total length",
        "average song length",
        "histogram of song lengths",
        "average album length",
        "average album track count",
    ]
    makePage(
        notebook,
        library,
        "artist",
        "options for a specific artist:",
        True,
        artistValues,
        artistOptions,
    )

    # year page
    yearValues = [
        "average release year",
        "histogram of release years",
    ]
    makePage(
        notebook,
        library,
        "year",
        "year options",
        False,
        yearValues,
        yearOptions,
    )


# progress bar on startup
initialize = tk.Frame()
dbProgress = ttk.Progressbar(initialize, length=200)
dbProgress.pack(padx=20, pady=20)

openButton = tk.Button(initialize, text="select music directory", command=open)
openButton.pack(padx=20, pady=20)

initialize.pack(expand=True)


# window geometry stuff
def center_window(window, w, h):
    window.update_idletasks()
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws - w) // 2
    y = (hs - h) // 2
    window.geometry(f"{w}x{h}+{x}+{y}")


root.resizable(False, False)
center_window(root, 400, 350)

# run window
root.mainloop()
