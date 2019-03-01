from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

import os
import sys
import platform
from Setlist import *
from string import capwords

from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
from database import *

from tkinter import Text as Text


# Open the database
engine = create_engine('sqlite:///songs.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

def getSonglist(songlist):
	""" Populates argument songlist with songs from directory """
	# Purges contents of the old treelist

	songlist.delete(*songlist.get_children())

	tag = "odd"
	song = []
	for row in session.query(Song):
		song.append(row.name)

	for song in sorted(song, key=str.lower):
		songlist.insert("", END, text=capwords(capwords(song)), tags=tag, 
			values=(capwords(session.query(Song).filter_by(name=song).first().artist), " "))

		if tag == "odd":
			tag = "even"
		else:
			tag = "odd"



	# 	root, ext = os.path.splitext(file_name)
	# 	if ext == ".txt":
	# 		songs.append(root)
	# songs = sorted(songs)
	# for song in songs:
	# 	songlist.insert(END, " " + song)


def savesong(name, filestring, top, oself, artist):
	# print(name)
	# print(filestring)
	file = open("song database/" + name + ".txt", "w+")
	file.write(filestring)
	file.close()
	top.destroy()

	# add to db
	song = Song(name.lower(), artist.lower(), name + ".txt")
	session.add(song)
	session.commit()

	getSonglist(oself.songlist)


def delete_song(top, name, filename):
	# print("name=" +name)
	song = session.query(Song).filter_by(name=name.lower()).first()
	# print(type(song))
	session.delete(song)
	session.commit()
	top.destroy()
	os.remove("song database/" + filename)

	messagebox.showinfo("Success", name + " was deleted")



class Application(Frame):

	def message(self):
		print("set built!")

	def newSongWindow(self, name="", contents=""):
		# print("New song!")
		top = Toplevel()
		top.title("New song")
		top.geometry("400x700")

		save_button = Button(top, text="Save", command=lambda: 
			savesong(songname_entry.get(), songtext.get("1.0", END), top, self, artist_entry.get()))

		close_button = Button(top, text="Close", command=top.destroy)

		# Labels
		label1 = Label(top, text="Name")
		label2 = Label(top, text="Artist")
		label3 = Label(top, text="Lyrics")

		# Text scrollbar
		scrollbar = Scrollbar(top)

		# Text field
		if (platform.system() == "Darwin"):
			songtext = Text(top, font=("Segoe UI", 14), yscrollcommand=scrollbar.set)
			print("Darwin!")

		else :
			songtext = Text(top, font=("Segoe UI", 9), yscrollcommand=scrollbar.set)


		songtext.insert(INSERT, contents)
		scrollbar.config(command=songtext.yview)

		# Entry
		# songname = StringVar(top, value=name+"")
		artist_entry = Entry(top)
		if name == "":
			artist_entry.insert(END, name)
		else :
			artist_entry.insert(END, capwords(session.query(Song).filter_by(name=name.lower()).first().artist))

		songname_entry = Entry(top)
		songname_entry.insert(END, name)

		for i in range(4):
			Grid.rowconfigure(top, i, weight=1)

		Grid.rowconfigure(top, 2, weight=5)
		Grid.columnconfigure(top, 1, weight=1)

		label1.grid(row=0, column=0, sticky=W, pady=5, padx=5)
		label2.grid(row=1, column=0, sticky=W, padx=5)
		label3.grid(row=2, column=0, stick=E+W+S, padx=5)

		songname_entry.grid(row=0, column=1, sticky=W+E, columnspan=2, padx=5)
		artist_entry.grid(row=1, column=1, sticky=W+E, columnspan=2, padx=5)

		songtext.grid(row=3, column=0, sticky=N+E+S+W, columnspan=3, padx=5)
		save_button.grid(row=4, column=1, pady=5, sticky=E)
		close_button.grid(row=4, column=2, padx=5, pady=5)
		scrollbar.grid(row=3, column=3, sticky=N+S+W)

	def viewtonew(self, name, contents, top):
		top.destroy()
		self.newSongWindow(name, contents)


	def viewSongWindow(self, name):
		# print("New song!")

		top = Toplevel()
		top.title("View song")
		top.geometry("400x700")
		filename = session.query(Song).filter_by(name=name.lower()).first().filename
		file = open("song database/" + filename)
		contents = file.read()

		close_button = Button(top, text="Close", command=top.destroy)
		edit_button = Button(top, text="Edit", command=lambda: self.viewtonew(name, contents, top))
		delete_button = Button(top, text="Delete", command=lambda: delete_song(top, name, filename))

		# Labels
		label1 = Label(top, text=name, font=("Calibri 12 bold"))
		label2 = Label(top, text="by "+capwords(session.query(Song).filter_by(name=name.lower()).first().artist))
		label3 = Label(top, text="Lyrics")

		# Text scrollbar
		scrollbar = Scrollbar(top)

		# Text field

		# fonts gotta be different for mac
		if (platform.system() == "Darwin"):
			songtext = Text(top, font=("Segoe UI", 14), yscrollcommand=scrollbar.set)
			print("Darwin!")

		else :
			songtext = Text(top, font=("Segoe UI", 9), yscrollcommand=scrollbar.set)

		songtext.insert(INSERT, contents)
		songtext.config(state=DISABLED)
		scrollbar.config(command=songtext.yview)

		for i in range(4):
			Grid.rowconfigure(top, i, weight=1)

		Grid.rowconfigure(top, 2, weight=5)
		Grid.columnconfigure(top, 1, weight=1)
		label1.grid(row=0, column=0, sticky=W, pady=5, padx=5, columnspan=4)
		label2.grid(row=1, column=0, sticky=E+W, padx=5)

		label3.grid(row=2, column=0, sticky=W)


		songtext.grid(row=3, column=0, sticky=N+E+S+W, columnspan=3, padx=5)
		delete_button.grid(row=4, column=0, sticky=E)
		edit_button.grid(row=4, column=1, pady=5, sticky=E)
		close_button.grid(row=4, column=2, padx=5, pady=5)
		scrollbar.grid(row=3, column=3, sticky=N+S+W)

	def makeset(self, songs, month, day, leader, setname):
		setlist = Setlist(setname, leader, month, day)
		setlist.addsongs(songs)
		setlist.createPowerpoint()
		# success box
		messagebox.showinfo("Success", "Build completed, powerpoint file created")



	def makeWidgets(self, master):

		# shortcut for typing ease
		master = self.master

		# Title of the window
		master.title("Powerpoint Generator")

		# Dimensions of the window
		master.geometry("900x500")

		# Styles
		# self.style = Style()
		# self.style.theme_use("default")

		# WIDGETS

		# Add label
		self.label1 = Label(master, text="Select songs")
		self.label2 = Label(master, text="Set Info")
		self.label3 = Label(master, text="Leader:")
		self.label4 = Label(master, text="Date")
		self.label5 = Label(master, text="Set name")
		self.label6 = Label(master, text="Setlist")

		# Scrollbar for listbox
		self.song_scrollbar = Scrollbar()

		# Add listbox
		# self.songlist = Listbox(master, yscrollcommand=self.song_scrollbar.set)

		# SONGLIST IS NOW TREEVIEW!!!
		self.songlist = Treeview(master, yscrollcommand=self.song_scrollbar.set)
		self.songlist["columns"] = ("artist")

		self.songlist.column("#0", width=50)
		self.songlist.column("artist", width=25)

		self.songlist.heading("#0", text="name")
		self.songlist.heading("artist", text="artist")

		getSonglist(self.songlist)
		
		
		
		# self.songlist.tag_configure("odd", background='orange')
		self.songlist.tag_configure("even", background="#E8E8E8")
		# Populate songs into listbox
		# getSonglist(self.songlist)

		# activate scrollbar
		self.song_scrollbar.config(command=self.songlist.yview)


		# songs = self.setlist.get(0, self.setlist.size()-1)
		# month = self.month.get()
		# day = self.day.get()
		# leader = self.leader.get()
		
		# Add buttons
		self.newsong_button = Button(master, text="New song", command=lambda:self.newSongWindow())

		self.build_button = Button(master, text="Build", command=lambda: 
							self.makeset(self.setlist.get(0, self.setlist.size()-1), self.month.get(), 
							self.day.get(), self.leader.get(), self.setname.get()))

		self.remove_button = Button(master, text="Remove", command=
							 lambda:self.setlist.delete(self.setlist.curselection()))

		self.view_button = Button(master, text="View", command=
								  lambda:self.viewSongWindow(self.songlist.
								  	item(self.songlist.selection(), "text")))

		# Add space for set
		self.setscroll = Scrollbar()
		self.setlist = Listbox(master, yscrollcommand=self.setscroll.set)
		self.setscroll.config(command=self.setlist.yview)

		# Entries

		# Set leader
		self.leader = StringVar()
		self.leader_entry = Entry(master, textvariable=self.leader)

		# Set name
		self.setname = StringVar()
		self.setname_entry = Entry(master, textvariable=self.setname)


		self.year = StringVar()
		self.year_entry = Entry(master, textvariable=self.year)

		# Option menus
		self.month = StringVar()

		months = ["January", "February", "March", "April", "May", "June",
				  "July", "August", "September", "October", "November",
				  "December"]
		self.month_menu = OptionMenu(master, self.month, months[0], *months)

		self.day = StringVar()
		days = range(1, 32, 1)
		self.days_menu = OptionMenu(master, self.day, days[0], *days)

		# Grid it!

		for j in range(7):
			Grid.columnconfigure(master, j, weight=1)
		# Grid.columnconfigure(master, 2, weight=1)

		for i in range(6):
			Grid.rowconfigure(master, i, weight=1)

		self.label1.grid(row=0, column=0, padx=5, pady=5, sticky=W)

		self.songlist.grid(row=1, column=0, padx=5, sticky=N+E+S+W, columnspan=3, rowspan=5, ipady=100, ipadx=100)
		self.song_scrollbar.grid(row=1, column=2, sticky=N+S+W, rowspan=5)

		self.newsong_button.grid(row=7, column=0, padx=5, pady=5, sticky=W+S+E)
		self.view_button.grid(row=7, column=1, padx=5, pady=5, sticky=W+S+E)
		self.remove_button.grid(row=7, column=4, sticky=S+W+E, padx=5, pady=5)
		self.build_button.grid(row=7, column=5, sticky=S+W+E, padx=5, pady=5)

		self.label2.grid(row=0, column=3, sticky=E, padx=10)
		self.label3.grid(row=1, column=3, sticky=E, padx=10)
		self.label5.grid(row=2, column=3, sticky=N+S+E, padx=10)
		self.label4.grid(row=3, column=3, sticky=N+S+E, padx=10)
		self.label6.grid(row=4, column=3, sticky=N+E, padx=10)

		self.leader_entry.grid(row=1, column=4, columnspan=2, sticky=E+W)

		self.setname_entry.grid(row=2, column=4, columnspan=2, sticky=E+W)

		self.month_menu.grid(row=3, column=4, sticky=W+E)
		self.days_menu.grid(row=3, column=5, sticky=W)
		self.setlist.grid(row=4, column=4, rowspan=3, columnspan=2, sticky=N+E+S+W)
		self.setscroll.grid(row=4, column=6, rowspan=3, sticky=W+N+S)

		# Event listeners!
		# self.songlist.bind("<Button-1>", lambda event: self.setlist.insert(END, self.songlist.get(ACTIVE)))

		self.songlist.bind("<Double-Button-1>", lambda event: self.setlist.insert(END, self.songlist.item(self.songlist.selection(), "text")))
		# self.setlist.bind("<ButtonRelease-1>", lambda event: print(self.setlist.get(self.setlist.curselection())))


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.makeWidgets(master)


def main():
	root = Tk()
	app = Application(root)
	app.mainloop()
	# root.destroy()


if __name__ == '__main__':
	main()
