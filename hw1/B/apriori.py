#!/usr/bin/env python

import itertools
import operator
import sys
baskets = []
current_itemsets = []
future_itemsets = []
tempSet = set()
candidateSet = set()


# count number of baskets that include input set
def countBasket(inputSet):
	counter = 0
	for basket in baskets:
		if(set(inputSet).issubset(basket)):
			counter = counter + 1
	return counter

# Caching data into baskets
for line in sys.stdin:
	line = line.strip() # trim spaces
	items = map(int, line.split()) # split string and map to int list
	baskets.append(items)
	
for index in range(100):
	tempSet.add(index + 1)

current_itemsets = itertools.combinations(tempSet, 2)
i = 2
resultSize = 0

while True:
	for itemset in current_itemsets:
		counter = countBasket(itemset)
		if(counter > 99):
			resultSize = resultSize + 1
			future_itemsets.append(itemset)
			if i > 2:
				for index in range(i):
					print(itemset[index]),
				print
	if(resultSize == 0):
		break
	
	del current_itemsets
	current_itemsets = []
		
	# generate candidates and placed into current itemsets
	for itemset in itertools.combinations(future_itemsets, 2):
		tupleA = itemset[0]
		tupleB = itemset[1]
		valid = True
		for index in range(i - 1):
			if tupleA[index] != tupleB[index]:
				valid = False
				break
		if valid and tupleA[i - 1] < tupleB[i - 1]:
			newTuple = tuple(sorted(set(tupleA) | set(tupleB)))
			current_itemsets.append(newTuple)
			
			
	# sort list
	for index in range(i + 1):
		current_itemsets.sort(key=operator.itemgetter(i - index))
	
	# clear future itemsets
	del future_itemsets
	future_itemsets = []
	
	resultSize = 0
	i = i + 1
