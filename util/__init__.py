from os.path import join, dirname, realpath
from re import findall
import numpy as np

def load_harvard_sentences(randomize = True):

	# get file pre-downloaded from CMU cite
	dir = dirname(realpath(__file__))
	fpath = join(dir, 'harvsents.txt')

	with open(fpath, 'r') as f:
		txt = f.read()
		sentences = findall("\d+\.\s(.+\.)", txt)

	# sentences come in lists of ten;
	# we want to preserve lists since they're phonetically balanced
	NUM = 10 # number of sentences per list
	assert(len(sentences) % NUM == 0)
	n_lists = len(sentences)//NUM
	lists = [sentences[i*NUM:(i+1)*NUM] for i in range(n_lists)]

	# but we do want to randomize the order of lists
	if randomize:
		np.random.shuffle(lists)
		for l in lists: # and order within lists
			np.random.shuffle(l)

	# flatten sentence list again now that shuffling is done
	sentences = [sentence for l in lists for sentence in l]
	return sentences
