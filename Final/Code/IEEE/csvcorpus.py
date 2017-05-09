from __future__ import with_statement

import logging
import csv
import itertools
import nltk
import re

from gensim import interfaces, utils
from collections import defaultdict

logger = logging.getLogger('gensim.corpora.csvcorpus')


class CsvCorpus(interfaces.CorpusABC):
    """
    Corpus in CSV format. The CSV delimiter, headers etc. are guessed automatically
    based on the file content.
    All row values are expected to be ints/floats.
    """

    def __init__(self, fname, labels):
        """
        Initialize the corpus from a file.
        `labels` = are class labels present in the input file? => skip the first column
        """
        logger.info("loading corpus from %s" % fname)
        self.fname = fname
        self.length = None
        self.labels = labels
        self.porter = nltk.PorterStemmer()
        self.stopwords = nltk.corpus.stopwords.words("english")
        self.label2id = {'Abstract': 10, 'Article Citation Count': 20, 'Author Affiliations': 2, 'Author Keywords': 15, 'Authors': 1, 'Copyright Year': 23, 'DOI': 13, 'Date Added To Xplore': 4, 'Document Identifier': 28, 'Document Title': 0, 'End Page': 9, 'IEEE Terms': 16, 'INSPEC Controlled Terms': 17, 'INSPEC Non-Controlled Terms': 18, 'ISBNs': 12, 'ISSN': 11, 'Issue': 7, 'Issue Date': 25, 'MeSH Terms': 19, 'Meeting Date': 26, 'Online Date': 24, 'PDF Link': 14, 'Patent Citation Count': 21, 'Publication Title': 3, 'Publisher': 27, 'ReferenceCount': 22, 'Start Page': 8, 'Volume': 6, 'Year': 5}
        self.id2label = {0: 'Document Title', 1: 'Authors', 2: 'Author Affiliations', 3: 'Publication Title', 4: 'Date Added To Xplore', 5: 'Year', 6: 'Volume', 7: 'Issue', 8: 'Start Page', 9: 'End Page', 10: 'Abstract', 11: 'ISSN', 12: 'ISBNs', 13: 'DOI', 14: 'PDF Link', 15: 'Author Keywords', 16: 'IEEE Terms', 17: 'INSPEC Controlled Terms', 18: 'INSPEC Non-Controlled Terms', 19: 'MeSH Terms', 20: 'Article Citation Count', 21: 'Patent Citation Count', 22: 'ReferenceCount', 23: 'Copyright Year', 24: 'Online Date', 25: 'Issue Date', 26: 'Meeting Date', 27: 'Publisher', 28: 'Document Identifier'}
        self.abstract = ["Abstract"]
        self.terms = ["Author Keywords", "IEEE Terms", "INSPEC Controlled Terms"]
        # load the first few lines, to guess the CSV dialect
        head = ''.join(itertools.islice(utils.smart_open(self.fname), 5))
        self.headers = csv.Sniffer().has_header(head)
        self.dialect = csv.Sniffer().sniff(head)
        logger.info("sniffed CSV delimiter=%r, headers=%s" % (self.dialect.delimiter, self.headers))

    def __iter__(self):
        """
        Iterate over the corpus, returning one sparse vector at a time.
        """
        reader = csv.reader(utils.smart_open(self.fname), self.dialect)
        # if self.headers:
        #     next(reader)    # skip the headers

        line_no = -1
        for line_no, line in enumerate(reader):
            # if self.labels:
            #     line.pop(0)  # ignore the first column = class label
            if line_no != 0:
                for label in self.abstract:
                    abstract_id = self.label2id[label]
                    abstract_tokens = self.tokenizer_absr(line[abstract_id])
                    abstract_tokens_no_sw = self.rm_sw(abstract_tokens)
                    abstract_corpora = self.stemmer(abstract_tokens_no_sw)
                    line[abstract_id] = map(lambda x: x.lower(), abstract_corpora)

                terms_dict = defaultdict(str)
                for label in self.terms:
                    term_id = self.label2id[label]
                    term_tokens = self.tokenizer_terms(line[term_id])
                    term_corpora = []
                    # build term dict: map stemmed version to original version for all term lists
                    terms_dict[label] = defaultdict(str)
                    for t in term_tokens:
                        term_corpora_tmp = ' '.join(self.stemmer(t))
                        term_corpora.append(term_corpora_tmp)
                        # build term dict: map stemmed version to original version for each term list
                        terms_dict[label][term_corpora_tmp] = ' '.join(t)
                    line[term_id] = map(lambda x: x.lower(), term_corpora)
                
                result_d = defaultdict(str)
                tmp_d = dict(enumerate(line))
                for k in tmp_d:
                    result_d[self.id2label[k]] = tmp_d[k]

                yield result_d, terms_dict

        self.length = line_no + 1  # store the total number of CSV rows = documents

    def tokenizer_absr(self, text):
        return re.findall("\w+", text)

    def tokenizer_terms(self, text):
        terms = text.split(";")
        return [self.tokenizer_absr(t) for t in terms]

    def rm_sw(self, tokens):
        return [w for w in tokens if w.lower() not in self.stopwords]

    def stemmer(self, tokens):
        return [self.porter.stem(token) for token in tokens]



