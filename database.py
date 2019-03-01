from sqlalchemy import *
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
import os
import string

engine = create_engine("sqlite:///songs.db", echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
s = Session()


class Song(Base):
	__tablename__ = "songs"

	id = Column(Integer, primary_key=True)
	name = Column("name", String, unique=True)
	artist = Column("artist", String)
	description = Column("description", String)
	speed = Column("speed", String)
	filename = Column("filename", String)
	sheetname = Column("sheetmusic doc name", String)

	def __init__(self, name, artist, filename, description=None,
				 speed=None, sheetname=None):

		self.name = name.lower()
		self.artist = artist.lower()
		self.filename = filename
		self.description = description
		self.speed = speed
		self.sheetname = sheetname

Base.metadata.create_all(engine)



def populate_from_folder():
	files = os.listdir(os.getcwd() + "/song database/")
	for filename in sorted(files, key=str.lower) :
		root, ext = os.path.splitext(filename)
		print(string.capwords(root))
		artist = input("Artist? ")
		song = Song(string.capwords(root), artist, filename)
		s.add(song)
		print()

	s.commit()

if __name__ == '__main__':
	song = s.query(Song).filter_by(artist="1").first()
	# s.delete(song)
	# s.commit()


