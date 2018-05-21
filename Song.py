import os
import sys


class Songfile(object):

    def __init__(self, songname, filename, artist="", path=(os.getcwd()+"/")):
        self.lyricArray = []

        self.path = path
        self.filename = filename
        self.songname = songname
        self.artist = artist

        songfile = open(self.path + self.filename, "r")
        self.lyricText = songfile.read() + "\n "

    def splitParts(self):
        # where the term part is a verse/chorus/prechorus or other
        # part of a song (idk tag maybe)

        # this will parse the string of the whole song and split
        # it into individual parts

        symbol = "~`!@#$%^&*()_-+={}[]:>;',</?*-+."

        lyricsleft = self.lyricText
        part = ""

        for i in range(len(lyricsleft)):
            if lyricsleft[i].isalnum() or lyricsleft[i] == " " or lyricsleft[i] in symbol:
                part += lyricsleft[i]

            elif lyricsleft[i] == "\n" and lyricsleft[i+1] == "\n":
                pass

            elif lyricsleft[i] == "\n" and (lyricsleft[i-1].isalnum()
                    or lyricsleft[i-1] in symbol or lyricsleft[i-1] == " "):
                part += lyricsleft[i]

            elif lyricsleft[i] == "\n" or i == len(lyricsleft)-1:
                self.lyricArray.append(part)
                print(part)
                part = ""

    def exportPowerpoint(self):
        createdFile = open("temp.txt", "w+")
        createdFile.write(self.songname + "\n\t" + self.artist + "\n\n")

        for part in self.lyricArray:
            endOfFirstLine = part.find("\n")
            # section = part[:endOfFirstLine]
            # if section[-1] == " ":
            #     section = section[:-1]

            # createdFile.write(self.songname + " (" + section + ")" + "\n\t")
            createdFile.write(self.songname + "\n\t")
            for letter in part[endOfFirstLine + 1:]:
                if letter != "\n":
                    createdFile.write(letter)
                else:
                    createdFile.write("\n\t")
            createdFile.write("\n\n")

        createdFile.close()
        os.rename("temp.txt", self.songname + ".ppt")
