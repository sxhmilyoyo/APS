import os, sys, getopt
from gensim import corpora, models

def get_topic_model(data_path, k):
	print data_path + '.mm'
	corpus = corpora.MmCorpus(data_path + '.mm')
	print data_path + '.dict'
	dictionary = corpora.Dictionary.load(data_path + '.dict')
	lda_model = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=k)
	lda_model.save(os.path.join(data_path, data_path+".lda"))
	print "lda model has been saved."

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hd:k:", ["domain=", "topic="])
	except:
		print "get_topic_model.py -d <domain> -k <topics>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print "get_topic_model.py -d <domain> -k <topics>"
			sys.exit()
		elif opt == "-d":
			domain = arg
		elif opt == "-k":
			k = int(arg)
	data_root = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE/"
	data_path = os.path.join(data_root, domain, domain.lower())
	print domain, "with", k, "topics"
	get_topic_model(data_path, k)

if __name__ == '__main__':
	main(sys.argv[1:])