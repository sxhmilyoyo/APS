import csvcorpus

class LDA:
	def __init__(self):
		self.data_path = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE"

	def load_corpus(self, corpus_raw):
		abstracts, terms = [], []
		for corpora, term in corpus:
			abstracts.append(corpora["Abstract"])
			terms.append(term)
		return abstracts, terms

	def build_dict(self, corpus_abstract):
		dictionary = corpora.Dictionary(corpus_abstract)
		dictionary.save()