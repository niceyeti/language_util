"""
Simple script for converting fbData files into sequences, where each line is a training sequence
for a recurrent neural language model of some kind.

"""
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import streams


def parse(ipath, opath, limit=-1):
	seqGen = streams.FbDataFileTokenStream(ipath, limit, fields=["title"], asSentences=True)

	if ".py" in opath or "fbdata" in opath.lower():
		raise Exception("ERROR: opath looks suspiciously like an fbdata or python file, to overwrite. Verify this was intended then comment out the exception check")

	with open(opath, "w+") as ofile:
		for seq in seqGen:
			ofile.write(seq+"\n")

def usage():
	print("Usage: python3 fbdata_to_sequences.py -ifile=[fb data path] -ofile=[output path]")
	print("Output file will consist of fb-data objects converted into single training sequences.")
	print("Each sequence represents a sentence from the object, and depends on how the og-object is parsed")

def main():
	ifile = ""
	ofile = ""
	limit = -1
	for arg in sys.argv:
		if "-ifile=" in arg:
			ifile = arg.split("=")[-1]
		if "-ofile=" in arg:
			ofile = arg.split("=")[-1]
		if "-limit=" in arg:
			limit = int(arg.split("=")[-1])

	if ifile == "":
		print("No input file passed")
		usage()
		exit()

	if ofile == "":
		print("No output file passed")
		usage()
		exit()

	parse(ifile, ofile, limit)













if __name__ == "__main__":
	main()



