from gensim import corpora
import os

class LDA():
	def __init__(self, data_domian):
		self.data_path = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE"
		self.data_domian = data_domian

	def load_corpus(self, corpus_raw):
		abstracts, terms = [], []
		for corpora, term in corpus_raw:
			abstracts.append(corpora["Abstract"])
			terms.append(term)
		return abstracts, terms

	def build_dict(self, corpus_abstract):
		dictionary = corpora.Dictionary(corpus_abstract)
		dictionary.save(os.path.join(slef.data_path, self.data_domian, self.data_domian.lower()+".dict"))
		print dictionary
		print dictionary.token2id
		return dictionary

	def convert_doc_bow(self, corpus_abstract):
		corpus_abstract_bow = [dictionary.doc2bow(corpora_abstract) for corpora_abstract in corpus_abstract]
		corpora.MmCorpus.serialize(os.path.join(self.data_path, self.data_domian, self.data_domian.lower()+".mm", corpus_abstract_bow))
		return corpus_abstract_bow
