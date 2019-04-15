"Trump" was removed from the positive word set for positive.txt/negative.txt, which are the Hu/Liu sentiment lexicon.

The lexicon "rankedPositives.txt"/"rankedNegatives.txt" is awesome, and was generated from word2vec the brute-force way,
by calculating the net-similarity of every word in big_model.d2v to a given positive/negative list from the Hu/Liu lexicon.
The algorithm is purely analytic:
	Input:
		-a large word2vec model @model
		-a modest (noisy, not huge ~1000-2000 words) lexicon @lexicon

	Method:
		for word in @model.vocab:
			word.similarity = 0.0
			for signal in @lexicon:
				word.similarity += @model.get_similarity(word, signal)

		return: @model.vocab sorted by similarity values

This method is exhaustive and slow-running, but does not require fancy machine learning, except what word2vec already does.
It is effectively just a slightly lower-dimensional (the word-vector size) version of calculating word similarities using the
full |vocab|x|vocab| co-occurrence matrix. Instead of full co-occurrence rows, we are comparing word-vectors.
The method is run separately for a specific lexicon (positive terms, negative terms, subjective terms), and simply returns
a ranking over words similar to the target signal lexicon.

Since @rankedNegatives.txt and @rankedPositives.txt were calculated over the entire vocabulary, one must determine a cutoff threshold
to classify terms as belonging to the respective set. That is, for all words in @rankedNegatives.txt, take only the first 3,000,
or apply some confidence metric.

ALSO, since these sets were generated independently, positive terms will be adjacent to negative ones, so the two lists need to be
merged by subtracting their similarity values accordingly. That is, word.similarity = positives[word].similarity - negatives[word].similarity,
then re-order each list. This should strengthen the self-similarity of lexical terms. This is done in the 
sentiment_cross_filter.py script, which outputs new lists filter_negatives.txt and filtered_positives.txt with their new values.
