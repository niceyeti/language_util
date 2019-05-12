"""

***GenSim implements a bunch of nice training data stream objects, for training from files of line-based
training sequences (sentences), and so forth. Moving stuff into ABLE/Sentinel could be as easy as
inheriting from those classes to implement ones that would read and preprocess headline objects
and so on. Use good practices and recognize that most of the etl boilerplate can probably be covered
via stream classes that perform all that internal logic. Think OOP.

Note that many of these generators can be chained: Use a fb-data parser to stream components of fb-data items to a file
as sentences, then use a file-line generator to feed those elsewhere.

"""

from ascii_text_normalizer import AsciiTextNormalizer
import sys
import re
import traceback

#Generates training sequences for word2vec based on sentences, splitting text on periods, questions, and exclamations: ".?!"
class FileSentenceStream(object):
	def __init__(self, fname, limit):
		"""
		@fname: The path to some file containing text which will be haphazardly broken into training sequences per-line.
		@limit: The number of sequences to generate before terminating the stream. If -1, then no limit (entire file).
		"""
		self._fname = fname
		self._limit = limit
		self._textNormalizer = AsciiTextNormalizer()

	#currently reads entire text file as a str, e.g. a novel or the like
	def __iter__(self):
		with open(self._fname, "r") as sequenceFile:
			sentences = sequenceFile.read().replace("!",".").replace("?",".").replace(";",".").split(".")
			normalizer = AsciiTextNormalizer()
			#print("Training on {} sentences".format(len(sentences)))

			for i, sentence in enumerate(sentences):
				seq = normalizer.NormalizeText(sentence, filterNonAlphaNum=True, deleteFiltered=True, lowercase=True).split()
				#print(seq)
				if len(seq) > 0 and (self._limit < 0 or i < self._limit):
					yield seq
				else:
					break

#Small class for memory-efficient line-based sequence generation from potentially large files.
#You could modify this to implement another scheme, such as sentence based streaming by splitting on periods instead of lines, etc.
#Might even be able to inherit from class File to implement a pure pythonic stream.
class FileLineStream(object):
	def __init__(self, fname, limit):
		"""
		@fname: The path to some file containing text which will be haphazardly broken into training sequences per-line.
		@limit: The number of sequences to generate before terminating the stream. If -1, then no limit (entire file).
		"""
		self._fname = fname
		self._limit = limit
		self._textNormalizer = AsciiTextNormalizer()

	def __iter__(self):
		with open(self._fname, "r") as sequenceFile:
			ct = 0
			for line in sequenceFile:
				if self._limit < 0 or ct < self._limit:
					yield line.lower().strip().split()
					#yield self._textNormalizer.NormalizeText(line).split()

class FbDataFileTokenStream(object):
	def __init__(self, fname, limit, fields=[], args=[]):
		"""
		This class is completely ad hoc for experimenting with how quickly gensim can build a model from a large ****-based fbData.py file.

		@fname: The path to some file containing text which will be haphazardly broken into training sequences per-line.
		@limit: The number of sequences to generate before terminating the stream. If -1, then no limit (entire file).
		@fields: The og_object fields (keys) whose values will be concatenated.
		@asSentences: If true, generator returns normalized sentences (sequences of words). Else, generates words (character sequences).

		@args: A list of arguments, defined over:
			--sentences to get output sequences as sentences; if not passed, generates sequences where each sequence is a word (sequence of chars)
			--filterNonAlphanum, --deleteFiltered, --lowercase: Arguments to NormalizeText(). These all default to False.
			--stopSymbol: If passed, every generated sequence will be terminated with the stop symbol. This is used to generate data for models
			that have a sense of sequence length/termination, e.g. finite horizon.
		"""
		self._fname = fname
		self._limit = limit
		self._fields = fields
		args = [arg.lower() for arg in args]
		self._asSentences = "--sentences" in args
		self._asLower = "--lower" in args or "--lowercase" in args
		self._deleteFiltered = "--deletefiltered" in args
		self._filterNonAlphaNum = "--filternonalphanum" in args
		self._useStopSymbol = "--stopsymbol" in args or "--stop" in args
		#Obviously, this has to be added after text normalization so it isn't filtered out
		self._stopSymbol = "."
		self._textNormalizer = AsciiTextNormalizer()
		if any([field not in ["title", "description"] for field in self._fields]):
			raise Exception("Invalid fields: {}. Only title and description are valid for og-objects.".format(fields))

	def _getText(self, ogDict):
		#from an og-object as a dict, returns the selected fields. If no fields, concatenates and returns the title and description
		if len(self._fields) == 0:
			text = ogDict["title"]+" "+ogDict["description"]
		else:
			text = ""
			if "title" in self._fields:
				text = ogDict["title"]
			if "description" in self._fields:
				text = text + " " + ogDict["description"]

		return self._textNormalizer.NormalizeText(text, filterNonAlphaNum=self._filterNonAlphaNum, deleteFiltered=self._deleteFiltered, lowercase=self._asLower)

	def _getSeq(self, text):
		#Only call this after text normalization
		if self._asSentences:
			seq = text
			if self._useStopSymbol:
				seq = seq + " " + self._stopSymbol
		else:
			seq = text.split()
			if self._useStopSymbol:
				seq.append(self._stopSymbol)
		return seq

	def __iter__(self):
		with open(self._fname, "r") as sequenceFile:
			ct = 0
			for line in sequenceFile:
				try:
					ogDict = eval(line)[1]["og_object"]
					if self._limit < 0 or ct < self._limit:
						text = self._getText(ogDict)
						seq = self._getSeq(text)
						ct += 1
						yield seq
					else:
						print("Generator exiting after yielding {} sequences".format(ct))
						break
				except:
					#traceback.print_exc()
					pass

