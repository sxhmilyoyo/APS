import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

def wordcloud(filename):
	# Read the whole text.
	text = open(os.path.join(filename, "wordcloud.txt")).read()

	# read the mask image
	# taken from
	# http://www.stencilry.org/stencils/movies/alice%20in%20wonderland/255fk.jpg
	alice_mask = np.array(Image.open(os.path.join(filename, "picture.jpg")))

	# stopwords = set(STOPWORDS)
	# stopwords.add("said")

	wc = WordCloud(background_color="white", max_words=2000, mask=alice_mask)
	# generate word cloud
	wc.generate(text)

	# store to file
	print "wordcloud.jpg has been saved."
	wc.to_file(os.path.join(filename, "wordcloud.jpg"))

	# show
	plt.imshow(wc, interpolation='bilinear')
	plt.axis("off")
	plt.figure()
	plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
	plt.axis("off")
	plt.show()

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hd:", ["domain="])
    except:
        print "wordcloud.py -d <domain>"
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print "wordcloud.py -d <domain>"
            sys.exit()
        elif opt == "-d":
            domain = arg
    data_root = "/usa/haoxu/Workplace/InfoLab/DataMining/Final_Project/Final/Data/IEEE/" + domain