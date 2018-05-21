import docx


class SongSheet(object):

    def __init__(self, name):
        doc = docx.Document(name)
        self.text = ""
        for paragraph in doc.paragraphs:
            self.text += paragraph.text + "\n"
        print (self.text)

    def transpose(self, numsteps):
        keys_sharp = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F",
                      "F#", "G", "G#"]
        keys_flat = ["A", "Bb", "B", "C", "Db", "D", "Eb", "E", "F",
                     "Gb", "G", "Ab"]
        chordTypes = ["m", "add", " ", "/", "sus"]  # concated to any numeric

		## Chords could be surrounded by brackets 

		output = ""

        for word in self.text.split():
            print(word)

			if word in keys_sharp:
				output += keys_sharp[(keys_sharp.index(word) + numsteps) % 12]

			elif word[1:] in chordTypes:
				if word[0:1] in keys_sharp:
					output += keys_sharp[(keys_sharp.index(word) + numsteps) % 12] + word[1:]
				elif word

			



goodgoodfather = SongSheet("Good Good Father.docx")
goodgoodfather.transpose(4)
