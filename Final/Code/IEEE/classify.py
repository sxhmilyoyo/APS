import json
import os, sys, getopt

def classify(filename):
	with open(filename) as fp:
		data = json.load(fp)
	res = {}
	for d in data:
		topic = data[d][0][0]
		if topic not in res:
			res[topic] = [d]
		else:
			res[topic].append(d)
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
	data_path = os.path.join(data_root, domain, "topic4doc_sorted.json")
	res = classify(data_path)
	with open(os.path.join(data_root, domain, "classification.json"), "w") as fp:
		json.dump(res, fp, indent=4)

if __name__ == '__main__':
	main(sys.argv[1:])