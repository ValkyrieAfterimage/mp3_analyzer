import os
from pathlib import Path
from mutagen.mp3 import MP3
import matplotlib.pyplot as plt
import datetime

# # how to access mutagen mp3 objects:
#
# file = MP3("Judee Sill - Judee Sill/08 - My Man on Love (Remastered).mp3")
# print(f"""
# title: {file.get("TIT2")}
# artist: {file.get("TPE1")}
# album: {file.get("TALB")}
# year: {file.get("TDRC")}
# track number: {file.get("TRCK")}
# length: {file.info.length}
# """)

# # UNIVERSAL FUNCTIONS


# clear terminal
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# convert 01:02:03 to 3723.0
def tts(time):
    return sum(float(x) * 60**i for i, x in enumerate(reversed(time.split(":"))))


# convert 3723.0 to 01:02:03
def stt(seconds):
    return str(datetime.timedelta(seconds=seconds))


# add each file to an array as an mp3 object (using the built in pathlib method which is no fun at all)
def mp3Array(path):
    library = []
    for i in path.glob("**/*.mp3"):
        library.append(MP3(i))
    return library


# # USER OPTION FUNCTIONS


# options that pop up on startup
def menu(library):
    clear()
    msg = """MAIN MENU

0: exit
1: general
2: albums
3: artists
4: years
"""
    print(msg)
    while True:
        try:
            option = int(input("select option: "))

            match int(option):
                case 0:
                    exit()
                case 1:
                    general(library)
                case 2:
                    sub(library, "album")
                case 3:
                    sub(library, "artist")
                case 4:
                    years(library)
                case _:
                    clear()
                    print(msg)
                    print("invalid input. dumb fuck")
        except ValueError:
            clear()
            print(msg)
            print("invalid input. dumb fuck")


# general info for *ALL* songs
def general(library):
    clear()
    msg = """GENERAL

0: back to main menu
1: total length
2: average song length
3: histogram of song lengths
4: average album length
5: average album track count
"""
    print(msg)
    while True:
        try:
            option = int(input("select option: "))

            clear()
            print(msg)

            match option:
                case 0:
                    menu(library)
                case 1:
                    print(
                        f"the total length of all songs in your library is {stt(totalLength(library))}"
                    )
                case 2:
                    print(
                        f"the average length of all songs in your library is {stt(average(library))}"
                    )
                case 3:
                    print("histogram opened. close window to continue")
                    lengthHistogram(library)
                case 4:
                    print(
                        f"the average length of all albums in your library is {stt(averageAlbumLength(library))}"
                    )
                case 5:
                    print(
                        f"the average track count of all albums in your library is {averageAlbumTrackCount(library)}"
                    )
                case _:
                    print("invalid input. dumb fuck")
        except ValueError:
            clear()
            print(msg)
            print("invalid input. dumb fuck")


# info for a specific artist OR album (dual purpose, fancy, right?)
def sub(library, type):
    if type == "album":
        tag = "TALB"
    if type == "artist":
        tag = "TPE1"
    else:
        print("what the fuck hath you wrought?")

    clear()

    # ask user for artist first
    while True:
        subValue = input(f"enter an {type}: ")
        subLibrary = []
        for i in library:
            if str(i.get(tag)).lower() == subValue.lower():
                subLibrary.append(i)
        if len(subLibrary) == 0:
            clear()
            print(f"{type} not found! try again...")
        else:
            break

    clear()
    msg = f"""{type.upper()}

0: back to main menu
1: total length
2: average song length
3: histogram of song lengths
"""
    print(msg)
    while True:
        try:
            print(f"current {type}: {subValue}")
            option = int(input("select option: "))

            clear()
            print(msg)

            match option:
                case 0:
                    menu(library)
                case 1:
                    if type == "album":
                        print(
                            f"the total length of all songs in {subValue} is {stt(totalLength(subLibrary))}"
                        )
                    else:
                        print(
                            f"the total length of all songs by {subValue} is {stt(totalLength(subLibrary))}"
                        )
                case 2:
                    if type == "album":
                        print(
                            f"the average length of all songs in {subValue} is {stt(average(subLibrary))}"
                        )
                    else:
                        print(
                            f"the average length of all songs by {subValue} is {stt(average(subLibrary))}"
                        )
                case 3:
                    print("histogram opened. close window to continue")
                    lengthHistogram(subLibrary)
                case _:
                    print("invalid input. dumb fuck")
        except ValueError:
            clear()
            print(msg)
            print("invalid input. dumb fuck")


# info about release years
def years(library):
    clear()
    msg = """YEARS

0: back to main menu
1: average year
2: histogram of years
"""
    print(msg)
    while True:
        try:
            option = int(input("select option: "))

            clear()
            print(msg)

            match option:
                case 0:
                    menu(library)
                case 1:
                    print(
                        f"the average release year of a song is {averageYear(library)}"
                    )
                case 2:
                    print("histogram opened. close window to continue")
                    yearHistogram(library)
                case _:
                    print("invalid input. dumb fuck")
        except ValueError:
            clear()
            print(msg)
            print("invalid input. dumb fuck")


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


# # # OLD STUFF
# # removed because I realized the information is only accurate if the song lengths are normally distributed
# # which they most definitely are NOT

# import numpy as np
# from scipy import stats

# # average and standard deviation
# avg = np.average([i.info.length for i in library])
# std = np.std([i.info.length for i in library])
# print(f"average: {stt(avg)}")
# print(f"standard deviation: {stt(std)}")

# # odds that a song will be longer than a certain value
# lengthToTest = "10:00"
# print(f"chance that a song will be longer than {lengthToTest}: {"%.4f" % (100*(1-stats.norm.cdf(tts(lengthToTest),avg,std)))}%")


# # STARTUP

# initialize database
clear()
print("now initializing database...")
library = mp3Array(Path("."))

# actually start the selection
menu(library)
