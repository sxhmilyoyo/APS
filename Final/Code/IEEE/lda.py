from gensim import corpora
import os
import json

class LDA():
	def __init__(self, data_domian):
		self.data_path = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE"
		self.data_domian = data_domian

	def load_corpus(self, corpus_raw):
		abstracts, terms = [], []
		for corpora, term in corpus_raw:
			abstracts.append(corpora["Abstract"])
			terms.append(term)
		with open(os.path.join(self.data_path, self.data_domian, "abstracts.json"), "w") as fp:
			json.dump(abstracts, fp, indent=4)
		print "abstracts.json has been saved."
		with open(os.path.join(self.data_path, self.data_domian, "terms.json"), "w") as fp:
			json.dump(terms, fp, indent=4)
		print "terms.json has been saved."
		return abstracts, terms

	def build_dict(self, corpus_abstract):
		dictionary = corpora.Dictionary(corpus_abstract)
		dictionary.save(os.path.join(self.data_path, self.data_domian, self.data_domian.lower()+".dict"))
		print self.data_domian.lower()+".dict has been saved."
		# print dictionary.token2id
		return dictionary

	def convert_doc_bow(self, dictionary, corpus_abstract):
		corpus_abstract_bow = [dictionary.doc2bow(corpora_abstract) for corpora_abstract in corpus_abstract]
		corpora.MmCorpus.serialize(os.path.join(self.data_path, self.data_domian, self.data_domian.lower()+".mm"), corpus_abstract_bow)
		print self.data_domian.lower()+".mm has been saved."
		return corpus_abstract_bow
