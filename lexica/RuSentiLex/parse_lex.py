"""
Parses the RuSentiLex file of csv sentiment language in the following format.
Only 'adj' terms marked positive or negative are output, and sent to positive.txt and negative.txt of raw signal terms.
NOTE: Cyrillic is preserved and text is not normalized; the lexicon is as given by RuSentiLex 
NOTE: Only single term signals are retained; the lexicon contains many multi-term phrases
	-blank lines are omitted
	-lines beginning with ! are comments
	-sentiment lines are words or phrases, as:
		аборт, Noun, аборт, negative, fact

	!RuSentiLex Structure
	!1. word or phrase,
	!2. part of speech or type of syntactic group,
	!3. initial word (phrase) in a lemmatized form,
	!4. Sentiment: positive, negative, neutral or positive/negative (indefinite, depends on the context),
	!5. Source: opinion, feeling (private state), or fact (sentiment connotation),
	!6. Ambiguity: if sentiment is different for senses of an ambiguous word, then sentiment orientations for all senses are described, the senses
	!are labeled with the RuThes concept names.
"""


lines = [line.strip() for line in open("rusentilex.txt","r").readlines() if len(line.strip()) > 0 and line[0] != "!"]
posFile = open("positive.txt", "w+")
negFile = open("negative.txt", "w+")
phraseCount = 0
wordCount = 0
posCount = 0
negCount = 0

for line in lines:
	tokens = line.split(",")
	if len(tokens) == 5:
		if " " not in tokens[0]: #eliminates phrases on the rhs
			wordCount += 1
			if "negative" in tokens[3].lower():
				negFile.write(tokens[0]+"\n")
				negCount += 1
			if "positive" in tokens[3].lower():
				posFile.write(tokens[0]+"\n")
				posCount += 1
		else:
			phraseCount += 1

print("{} phrase count {} word count, {} positives {} negatives".format(phraseCount, wordCount, posCount, negCount))
posFile.close()
negFile.close()

