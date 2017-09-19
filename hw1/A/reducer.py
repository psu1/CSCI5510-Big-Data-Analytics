#!/usr/bin/env python
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
author_dict = {}

for line in sys.stdin:
	line = line.strip()
	word, count = line.split('\t', 1)
	try:
		count = int(count)
	except ValueError:
		continue
	if current_word == word:
		current_count += count
	else:
		if current_word:
			author_dict[current_word] = current_count
		current_count = count
		current_word = word
author_dict[current_word] = current_count

for key, value in author_dict.iteritems():
	print('%s\t%s' % (key, value))