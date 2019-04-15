"""
Converts the cross-filtered ranked lists to simple word lists,
where the ranked lists are tuples as: ('+', 'stateoftheart', 106.93565581503208)
"""

posFile = open("./lexicon/rankedPositives.txt", "r")
negFile = open("./lexicon/rankedNegatives.txt", "r")

limit = 5000

positives = [eval(line.strip())[1] for line in posFile.readlines()][0:limit]
negatives = [eval(line.strip())[1] for line in negFile.readlines()][0:limit]

#cross filter
#print("Cross filtering...")
#positives = [pos for pos in positives if pos not in negatives][0:limit] #note this removes ambiguous words from positives, not vice versa; negative terms tend to have better signal characteristics, so keep em
#negatives = [neg for neg in negatives if neg not in positives][0:limit]


open("./lexicon/temp/positive.txt", "w+").write("\n".join(positives))
open("./lexicon/temp/negative.txt", "w+").write("\n".join(negatives))











