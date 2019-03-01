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
	

class Application(Frame):

	def makeWidgets(self, master):

		# shortcut for typing ease
		master = self.master

		# Title of the window
		master.title("Edit Database")

		# Dimensions of the window
		master.geometry("700x500")

		# Scrollbar for listbox
		self.list_scrollbar = Scrollbar()


		# CREATES "TREEVIEW" WIDGET WHICH IS BASICALLY A TABLE
		self.tree = Treeview(master, yscrollcommand=self.list_scrollbar.set)
		self.tree["columns"] = "artist"

		self.tree.column("#0", width=50)
		self.tree.column("artist", width=25)

		self.tree.heading("#0", text="name")
		self.tree.heading("artist", text="artist")

		for row in session.query(Song):
			self.tree.insert("", END, text=capwords(row.name), values=(capwords(row.artist), " "))
			print(row.artist)


		# ADD ONTO FELTBOARD
		self.list_scrollbar.pack(side=RIGHT, fill=BOTH)
		self.tree.pack(fill=BOTH, expand=True)

	


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