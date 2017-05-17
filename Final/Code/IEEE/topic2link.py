import json
import os, sys, getopt

def get_topic2link(filename1, filename2):
	with open(filename1) as fp:
		data = json.load(fp)
	with open(filename2) as fp:
		links = json.load(fp)
	res = {}
	for t in data:
		res[t] = []
		docids = data[t]
		for docid in docids:
			res[t].append(links[int(docid)-1])
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
	data_path_1 = os.path.join(data_root, domain, "classification.json")
	data_path_2 = os.path.join(data_root, domain, "links.json")
	res = get_topic2link(data_path_1, data_path_2)
	with open(os.path.join(data_root, domain, "topic2link.json"), "w") as fp:
		json.dump(res, fp, indent=4)

if __name__ == '__main__':
	main(sys.argv[1:])