from tkinter import *
from tkinter.ttk import *
import os


def getSonglist():
    """ Returns array containing songs in given folder """
    songs = []
    for file_name in os.listdir(os.getcwd() + "/song database/"):
        root, ext = os.path.splitext(file_name)
        if ext == ".txt":
            songs.append(root)
    return sorted(songs)

    # return [
    #     "One Way",
    #     "Your Grace is Enough",
    #     "Good Good Father",
    #     "How He Loves",
    #     "Beauty For Ashes"
    #     ]


class Application(Frame):

    def message(self):
        print("set built!")

    def makeWidgets(self, master):

        # shortcut for typing ease
        master = self.master

        # Title of the window
        master.title("Powerpoint Generator")

        # Dimensions of the window
        master.geometry("500x400")

        # Styles
        # self.style = Style()
        # self.style.theme_use("default")

        # FRAMES

        # Top frame
        self.main_frame = Frame(self, relief=RAISED, borderwidth=1)
        self.main_frame.pack(fill=BOTH, expand=True)
        self.pack(fill=BOTH, expand=True)

        # Left frame
        self.left_frame = Frame(self)
        self.left_frame.pack(fill=Y, expand=True)

        # WIDGETS

        # Add label
        self.label1 = Label(self.main_frame, text="Select songs")
        self.label1.pack()

        # Scrollbar for listbox
        self.song_scrollbar = Scrollbar(self.main_frame)

        # Add listbox
        self.songlist = Listbox(self.main_frame, yscrollcommand=self.song_scrollbar.set)
        self.songlist.pack(side=LEFT, fill=Y)

        # activate scrollbar
        self.song_scrollbar.config(command=self.songlist.yview)
        self.song_scrollbar.pack(side=LEFT, fill=Y)

        # populate listbox with songs in specific directory
        for song in getSonglist():
            self.songlist.insert(END, song)

        # Add buttons

        self.newsong_button = Button(master, text="New song", command=None)
        self.newsong_button.pack(side=LEFT, padx=5, pady=5)

        self.build_button = Button(master, text="Build", command=None)
        self.build_button.pack(side=RIGHT, padx=5, pady=5)

        self.remove_button = Button(master, text="Remove", command=None)
        self.remove_button.pack(side=RIGHT)

        # self.master.title("Buttons")
        # self.style = Style()
        # self.style.theme_use("default")

        # frame = Frame(self, relief=RAISED, borderwidth=1)
        # frame.pack(fill=BOTH, expand=True)

        # self.pack(fill=BOTH, expand=True)

        # closeButton = Button(self, text="Close")
        # closeButton.pack(side=RIGHT, padx=5, pady=5)

        # okButton = Button(self, text="OK")
        # okButton.pack(side=RIGHT)

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.makeWidgets(master)


def main():
    root = Tk()
    app = Application(root)
    app.mainloop()
    # root.destroy()


if __name__ == '__main__':
    main()
