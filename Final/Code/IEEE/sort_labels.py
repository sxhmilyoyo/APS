import operator
import json
import os, sys, getopt

def sort_labels(filename):
	with open(filename) as fp:
		data = json.load(fp)
	res = {}
	for d in data:
		sorted_label = sorted(data[d].items(), key=operator.itemgetter(1), reverse=True)
		res[d] = sorted_label
	return res

def main(argv):
	try:
		opts, args = getopt.getopt(argv, "hd:")
	except:
		print "get_topic_model.py -d <domain> -k <topics>"
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-h":
			print "get_topic_model.py -d <domain> -k <topics>"
			sys.exit()
		elif opt == "-d":
			domain = arg
	data_root = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE/"
	data_path = os.path.join(data_root, domain, "topic4doc.json")
	res = sort_labels(data_path)
	with open(os.path.join(data_root, domain, "topic4doc_sorted.json"), "w") as fp:
		json.dump(res, fp, indent=4)

if __name__ == '__main__':
	main(sys.argv[1:])