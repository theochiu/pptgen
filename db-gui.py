from tkinter import *
from tkinter.ttk import *
import os
import sys
from database import *
from string import capwords

# Open the database
engine = create_engine('sqlite:///songs.db', echo=True)
 
# create a Session
Session = sessionmaker(bind=engine)
session = Session()

def getdb(alist, attr):
	""" Populates argument songlist with songs from directory """
	# Purges contents of the old listbox
	alist.delete(0, END)
	queries = []
	for row in session.query(Song):
		queries.append(capwords(getattr(row, attr)))

	for query in queries:
		alist.insert(END, " " + query)

def switch(button):
	button.config(text="Off")

def getSonglist(songlist):
	""" Populates argument songlist with songs from directory """
	# Purges contents of the old treelist

	songlist.delete(*songlist.get_children())

	tag = "odd"
	song = []
	for row in session.query(Song):
		song.append(row.name)

	for song in sorted(song, key=str.lower):
		obj = session.query(Song).filter_by(name=song).first()
		songlist.insert("", END, text=capwords(song), tags=tag, 
			values=(capwords(obj.artist), obj.filename, obj.description,
				obj.speed, obj.sheetname))

		if tag == "odd":
			tag = "even"
		else:
			tag = "odd"
	

class Application(Frame):

	def makeWidgets(self, master):

		# shortcut for typing ease
		master = self.master

		# Title of the window
		master.title("Edit Database")

		# Dimensions of the window
		master.geometry("900x450")

		# Scrollbar for listbox
		self.list_scrollbar = Scrollbar()


		# CREATES "TREEVIEW" WIDGET WHICH IS BASICALLY A TABLE
		self.tree = Treeview(master, yscrollcommand=self.list_scrollbar.set)
		self.tree["columns"] = "artist", "filename", "description", "speed", "sheetname"

		self.tree.column("#0", width=250)
		self.tree.column("artist", width=200)
		self.tree.column("filename", width=200)
		self.tree.column("description", width=25)		
		self.tree.column("speed", width=25)
		self.tree.column("sheetname", width=25)		


		self.tree.heading("#0", text="name")
		self.tree.heading("artist", text="artist")
		self.tree.heading("filename", text="filename")
		self.tree.heading("description", text="description")
		self.tree.heading("speed", text="speed")
		self.tree.heading("sheetname", text="sheetname")

		getSonglist(self.tree)


		# ADD ONTO FELTBOARD
		self.list_scrollbar.pack(side=RIGHT, fill=BOTH)
		self.tree.pack(fill=BOTH, expand=True)

		# LISTENERS 
		# self.tree.bind("<Double-Button-1>", lambda event: self.setlist.insert(END, self.songlist.item(self.songlist.selection(), "text")))

	


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