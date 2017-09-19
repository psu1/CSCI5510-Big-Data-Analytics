#!/usr/bin/env python

import sys
for basket in range(10000):
	# We only consider 1-100 because items > 100 cannot
	# be included in the baskets for more than 100 times
	# e.g. Item 1 appears in 10000 baskets
	#      Item 2 appears in 5000  baskets
	# i.e. Item i appears in 10000 / i baskets
	# Therefore, for n > 100, 10000 / n < 100
	for item in range(100): 
		if(item > basket): break
		if((basket + 1) % (item + 1) == 0):
			print(item + 1), 
	sys.stdout.flush()
	print('') # new line