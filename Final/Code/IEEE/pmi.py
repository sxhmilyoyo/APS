import json
import os, sys, getopt
import math

def probability(t1, t2, abstracts_unigram, abstracts_bigram):
	num = 0
	if len(abstracts_unigram) != len(abstracts_bigram):
		print "length not equal!!!"
		sys.exit()
	abstracts_len = len(abstracts_unigram)
	if t1 and t2:
		# print t1, t2
		for i in range(abstracts_len):
			if t1 in abstracts_unigram[i] and t2 in abstracts_bigram[i]:
				num += 1
	elif t1:
		# print t1, t2
		for i in range(abstracts_len):
			if t1 in abstracts_unigram[i]:
				num += 1
	elif t2:
		# print t1, t2
		for i in range(abstracts_len):
			if t2 in abstracts_bigram[i]:
				num += 1
	return float(num) / abstracts_len

def pmi(t1, t2, abstracts_unigram, abstracts_bigram):
	p1 = probability(t1, None, abstracts_unigram, abstracts_bigram)
	p2 = probability(None, t2, abstracts_unigram, abstracts_bigram)
	p1_2 = probability(t1, t2, abstracts_unigram, abstracts_bigram)
	if p1 == 0 or p2 == 0 or p1_2 == 0:
		return 0
	return math.log((p1_2 / (p1 * p2)), 2)

def get_topics(filename):
	with open(filename) as fp:
		topics = json.load(fp)
	res = {}
	for t_key in topics:
		res[t_key] = [k for k in topics[t_key]]
	return res

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hd:", ["domain="])
	except:
		print "get_topic_model.py -d <domain>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print "get_topic_model.py -d <domain>"
			sys.exit()
		elif opt == "-d":
			domain = arg

	data_root = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE"
	print "Addressing", os.path.join(data_root, domain, "abstracts.json")
	with open(os.path.join(data_root, domain, "abstracts.json")) as fp:
		abstracts_unigram = json.load(fp)
	with open(os.path.join(data_root, domain, "bigram.json")) as fp:
		abstracts_bigram = json.load(fp)
	with open(os.path.join(data_root, domain, "labels_short.json")) as fp:
		labels = json.load(fp)
	topics = get_topics(os.path.join(data_root, domain, "topics.json"))

	result = {}
	# for label in labels:
	# 	result[label] = {}
	# 	for t_k in topics:
	# 		sumv = 0
	# 		for term in topics[t_k]:
	# 			sumv += pmi(term, label, abstracts_unigram, abstracts_bigram)
	# 		result[label][t_k] = sumv
	for t_k in topics:
		print "topic:", t_k
		result[t_k] = {}
		label_num = 1
		for label in labels:
			print "label:", label_num
			sumv = 0
			for term in topics[t_k]:
				sumv += topics[t_k][term] * pmi(term, label, abstracts_unigram, abstracts_bigram)
			result[t_k][label] = sumv
			label_num += 1

		with open(os.path.join(data_root, domain, t_k+"_pmi.json"), "w") as fp:
			json.dump(result, fp, indent=4)
		print "pmi.json has been saved."

if __name__ == '__main__':
	main(sys.argv[1:])
