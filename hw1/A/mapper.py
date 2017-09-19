#!/usr/bin/env python

import sys
import itertools

if __name__ == '__main__':
	for line in sys.stdin:
		line = line.strip()
		authors = line.split('\t')
		for author_set in itertools.combinations(set(authors), 2):
			if author_set[0] < author_set[1]:
				print('"%s" "%s"\t%s' % (author_set[0], author_set[1], 1))
			else:
				print('"%s" "%s"\t%s' % (author_set[1], author_set[0], 1))
