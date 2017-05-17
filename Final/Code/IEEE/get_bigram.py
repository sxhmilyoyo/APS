import json
import os, sys, getopt
         
def getNgram(ng, trainingData):
    """
    This function builds the n-gram and the frequency dictionary of the each n-gram
    """
    nGrams = []
    for n in range(2, ng + 1):
        for i in range(len(trainingData) - n + 1):
            nGram = trainingData[i:i + n]
            nGrams.append(' '.join(nGram))
    return nGrams
        
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

    with open(os.path.join(data_root, domain, "abstracts.json")) as fp:
        abstracts = json.load(fp)

    ngrams = []
    print "getting n-gram......",
    for abstract in abstracts:
        ngram = getNgram(2, abstract)
        ngrams.append(ngram)
    print "finished."
    # store the frequency dictionary to the local
    with open(os.path.join(data_root, domain, "bigram.json"), "w") as fp:
        json.dump(ngrams, fp, indent=4)
    print "bigram.json has been stored."

if __name__ == '__main__':
    main(sys.argv[1:])