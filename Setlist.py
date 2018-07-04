import sys
import os
from Song import *


def deleteAllPowerpoints():
    for file_name in os.listdir(os.getcwd() + "/"):
        root, ext = os.path.splitext(file_name)
        if ext == ".ppt":
            os.remove(file_name)


class Setlist(object):

    default_path = os.getcwd() + "/song database/"

    def __init__(self, setName, leader=""):
        self.setName = setName
        self.leader = leader
        self.songs = []

    @classmethod
    def searchDirectory(cls, name, path=default_path):
        # returns name of the text file that has the title of the song in it
        name = str(name).lower()
        for file_name in os.listdir(path):
            root, ext = os.path.splitext(file_name)
            root = root.lower()

            if ext != ".txt":
                pass
            elif name.replace(" ", "") in root.replace(" ", ""):
                # triggered if the name passed without spaces is in the
                # filename without spaces deals properly with parens
                return file_name

        raise "Requested text file not found"

    def getLeader(self):
        print(self.leader)
        return self.leader

    def getSetName(self):
        print(self.setName)
        return self.setName

    def addsongs(self, songs):
        for song in songs:
            print(song)
            self.songs.append(Songfile(song, self.searchDirectory(song, self.default_path), path=self.default_path))

    def createPowerpoint(self, path=(os.getcwd() + "/")):
        # look for each song in songs[] in the directory
        # accomodating for differnt naming conventions
        # use powerpoint method in songfile class to create powerpoints for
        # each song merge all the powerpoints together

        # creates powerpoints for every song in the set
        for song in self.songs:
            song.splitParts()
            song.exportPowerpoint()

        # merges all the ppts into a temp file
        temp = open("temp.txt", "w+")
        temp.write(self.setName + "\n\n\tGenerated with SlideMaker")
        temp.write("\n\tby: " + self.leader + "\n")

        for song in self.songs:
            f = open(path + song.songname + ".ppt", "r")
            temp.write(f.read() + "\n\n\n")
            f.close()
            os.remove(path + song.songname + ".ppt")

        temp.close()

        num = 1
        name = self.setName + " (Worship Slides)" + ".ppt"
        while name in os.listdir():
            name = self.setName + " (Worship Slides " + str(num) + ")" + ".ppt"
            if name in os.listdir():
                num += 1

        os.rename("temp.txt", name)
