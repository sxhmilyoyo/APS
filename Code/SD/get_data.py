import os
import json
import bibtexparser

def get_data(filename):
	with open(filename) as fp:
		raw_data = fp.read()

	b = bibtexparser.loads(raw_data)
	data = b.entries
	res = []
	for item in data:
		d = {}
		title = item.get("title", None)
		author = item.get("author", None)
		abstract = item.get("abstract", None)
		keyword = item.get("keyword", None)

		d["title"] = title
		d["author"] = author
		d["abstract"] = abstract
		d["keyword"] = keyword

		res.append(d)
	return res

if __name__ == '__main__':
	data_root = "../Data"
	
	ir = get_data(os.path.join(data_root, "ir.bib"))
	ml = get_data(os.path.join(data_root, "ml.bib"))
	
	with open(os.path.join(data_root, "ir.json"), "w") as fp:
		json.dump(ir, fp, indent=4)

	with open(os.path.join(data_root, "ml.json"), "w") as fp:
		json.dump(ml, fp, indent=4)
