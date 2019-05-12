"""
Simple script for converting fbData files into sequence files, where each line is a training sequence
for language modeling of some kind.
"""
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import streams


def parse(ipath, opath, limit=-1, params=[], fields=["title"]):
	if not any(field in fields for field in ["title", "description"]):
		raise Exception("Fields invalid. Only 'title' and 'description' are acceptable.")

	seqGen = streams.FbDataFileTokenStream(ipath, limit, fields=fields, args=params)
	if ".py" in opath or "fbdata" in opath.lower():
		raise Exception("ERROR: opath looks suspiciously like an fbdata or python file, to overwrite. Verify this was intended then comment out the exception check")

	with open(opath, "w+") as ofile:
		for seq in seqGen:
			ofile.write(seq+"\n")

def usage():
	print("Usage: python3 fbdata_to_sequences.py -ifile=[fb data path] -ofile=[output path] -limit=[num sequences] [optional params]")
	print("Output file will consist of fb-data objects converted into single training sequences.")
	print("Each sequence represents a sentence from the object, and depends on how the og-object is parsed")
	print("Output params (not stable, subject to change, but most are text parsing params):")
	print("    --deleteFiltered, --filterNonAlphaNum, --lowercase, --sentences, --stopSymbol")
	print("    See FbDataFileTokenStream and NormalizeText() function for a description of these params, since they are unstable (not maintained here)")
	print("    --stopSymbol: If present, sequences will be ended with the stop symbol. This data is used to train sequential models with finite horizons")
	print("    -fields=[list of fields] Valid fields are currently just 'title' and 'description'")
	print("Suggested: python3 fbdata_to_sequences.py -ifile=../[somepath]/fbData.py -ofile=./seq_desc.txt -limit=250000 --deleteFiltered --lowercase --filterNonAlphaNum --sentences --stopSymbol -fields=description")
	print("Then: cat seq_desc.txt | sort | uniq > final_output.txt")

def main():
	ifile = ""
	ofile = ""
	limit = -1
	# Text parsing params; includes those defined in FbDataFileTokenStream and (inside it) the paras passed to NormalizeText()
	params = []
	fields = ["title"] #default
	for arg in sys.argv:
		if "-ifile=" in arg:
			ifile = arg.split("=")[-1]
		if "-ofile=" in arg:
			ofile = arg.split("=")[-1]
		if "-limit=" in arg:
			limit = int(arg.split("=")[-1])
		if "-fields=" in arg:
			fields = arg.split("=")[-1].split(",")

	if not any(field in ["title","description"] for field in fields):
		raise Exception("No valid fields in {}. Valid fields are 'title' and 'description'")

	args = [arg.lower() for arg in sys.argv]
	params = []
	if "--sentences" in args:
		params.append("--sentences")
	if "--lowercase" in args:
		params.append("--lowercase")
	if "--filternonalphanum" in args:
		params.append("--filterNonAlphaNum")
	if "--deletefiltered" in args:
		params.append("--deleteFiltered")
	if "--stopsymbol" in args:
		params.append("--stopSymbol")

	print("Generation params: "+str(params))

	if ifile == "":
		print("No input file passed")
		usage()
		exit()

	if ofile == "":
		print("No output file passed")
		usage()
		exit()

	parse(ifile, ofile, limit, params)













if __name__ == "__main__":
	main()



