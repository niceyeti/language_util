"""
This is not the gold standard implementation. See **** or Cheetah. Critical updates must be reflect there as well.

A wrapper around a word2vec implementation for experimental usage only, just playing
around with different implementations for evaluation.

The code libraries used are the property of their respective authors.


***GenSim implements a bunch of nice training data stream objects, for training from files of line-based
training sequences (sentences), and so forth. Moving stuff into ABLE/Sentinel could be as easy as
inheriting from those classes to implement ones that would read and preprocess headline objects
and so on. Use good practices and recognize that most of the etl boilerplate can probably be covered
via stream classes that perform all that internal logic. Think oop.
"""

from ascii_text_normalizer import AsciiTextNormalizer
import sys
import re
import gensim
import traceback
from random import shuffle
from streams import *

stopwords = [w.strip() for w in open("./lexicon/stopwords.txt", "r").readlines()]

def Train():
	vecModel = gensim.models.Word2Vec(seqStream, size=vecSize, window=windowSize, iter=numIterations, min_count=minTermFrequency, workers=workers, sg=(model == "SKIPGRAM"))

def isValidCmdLine():
	isValid = False

	if len(sys.argv) < 3:
		print("Insuffiient cmd line parameters")	
	elif not any("-fname=" in arg for arg in sys.argv):
		print("No fname passed")
	elif not any("-stream=" in arg for arg in sys.argv):
		print("No stream passed")
	elif not any("-trainLimit=" in arg for arg in sys.argv):
		print("No training-example limit passed")
	elif not any("-iter=" in arg for arg in sys.argv):
		print("No n-iterations params passed")
	else:
		isValid = True

	return isValid

def usage():
	print("Usage: python3 ./Word2Vec.py\n\t-fname=[path to line-based training txt file]\n\t-trainLimit=[num training sequences to extract from file; pass -1 for no limit]")
	print("\t-iter=[num iterations]")
	print("\t-vecSize=[feature vector size]")
	print("\t-minFreq=[minimum term frequency]")
	print("\t-model=[CBOW, SKIPGRAM]")
	print("\t-stream=[SENTENCE, FBDATA, or NEWLINE] Sentence will generate sequences from sentence, newline from file lines, fbdata from og_object parsing.")
	print("\t-windowSize=[training window size]")
	print("\t-validationLexicon=[path to some lexicon]")
	print("\t-sentimentLexiconFolder=[path to folder containing positive.txt and negative.txt]")
	print("Author recommends window size=10 for skipgram, 5 for CBOW word2vec models; this likely also applies to doc2vec.")
	print("According to wikipedia (unattributed), 'Typically, the dimensionality of the vectors is set to be between 100 and 1,000'.")
	print("Example: python3 Word2Vec.py -fname=../mldata/treasureIsland.txt -trainLimit=-1 -iter=10 -vecSize=200 -minFreq=3 -stream=SENTENCE -windowSize=10 -model=CBOW")
	print("-validationLexicon is just an idea I had, for bulding models that target a specific kind of language property. Given that you have")
	print("a lexicon describing that property (e.g., positive or negative words), one can qualitatively evaluate word2vec based on how similarly")
	print("it ranks the terms within that cluster, defined as the n**2 sum similarity of those terms with eachother. HOWEVER, these values can grow")
	print("unbounded if gensim overfits, effectively just increasing the magnitude of all vectors, hence their sum will increase w/out bound. The")
	print("method for mitigating this effect is to score the 'coherence' metric (given a lexicon) by evaluating the ranking of similarity over these")
	print("terms, instead of their numerical 'similarity' given by gensim.")

def main():
	if not isValidCmdLine():
		print("Insufficient/incorrect args passed, see usage.")
		usage()
		return -1

	print("Author recommends window size=10 for skipgram, 5 for CBOW word2vec models; this likely also applies to doc2vec.")
	print("According to wikipedia (unattributed), 'Typically, the dimensionality of the vectors is set to be between 100 and 1,000',")
	print("but optimize as with any hyper-parameter. Optimization can be done by Cheetah method or similar, for ")

	fname = ""
	windowSize = 5
	vecSize = 100
	minTermFrequency = 3
	workers = 1
	CBOW = "CBOW"
	SKIPGRAM = "SKIPGRAM"
	validModels = {CBOW, SKIPGRAM, "SKIP"}
	model = ""
	limit = -1
	numIterations = 10
	minTermFrequency = 5
	SENTENCE = "SENTENCE"
	NEWLINE = "NEWLINE"
	FBDATA = "FBDATA"
	validStreams = {SENTENCE, NEWLINE, FBDATA}
	stream = ""
	opath = ""
	validationLexiconPath = ""
	sentimentLexiconFolder = ""
	for arg in sys.argv:
		if "-fname=" in arg:
			fname = arg.split("=")[-1]
		if "-trainLimit=" in arg:
			limit = int(arg.split("=")[-1])
		if "-iter=" in arg or "-numIter=" in arg:
			numIterations = int(arg.split("=")[-1])
		if "-minFreq=" in arg:
			minTermFrequency = int(arg.split("=")[-1])
		if "-stream=" in arg:
			stream = arg.split("=")[-1].upper()
		if "-model=" in arg:
			model = arg.split("=")[-1].upper()
		if "-window=" in arg or "-windowSize=" in arg:
			windowSize = int(arg.split("=")[-1])
		if "-vecSize=" in arg:
			vecSize = int(arg.split("=")[-1])
		if "-ofile=" in arg or "-opath" in arg:
			opath = arg.split("=")[-1]

	if stream not in validStreams:
		print("No valid stream passed: {}".format(validStreams))
		usage()
		exit()
	elif stream == "FBDATA": #this is just a hack to see how quickly large amounts of fb content can be trained
		seqStream = FbDataFileStream(fname, limit)
	elif stream == "NEWLINE":
		seqStream = FileLineStream(fname, limit)
	elif stream == "SENTENCE":
		seqStream = FileSentenceStream(fname, limit)

	if model not in validModels:
		print("No valid model passed: {}".format(validModels))
		usage()
		exit()

	try:
		vecModel = gensim.models.Word2Vec(seqStream, size=vecSize, window=windowSize, iter=numIterations, min_count=minTermFrequency, workers=workers, sg=(model == "SKIPGRAM" or model == "SKIP"))
	except:
		traceback.print_exc()
		print("Caught exception. If you're getting a 'build vocabulary' type error, you're stream/generator is probably broken and passing empty lists or similar")

	print("Training completed")

	if opath != "":
		print("Writing model to "+opath)
		vecModel.save(opath)

if __name__ == "__main__":
	main()


