#!/usr/bin/env python

import sys
import cStringIO
import re
buff = None
article_started = False
counter = 0
for line in sys.stdin:
	line = line.strip()
	if '<author' in line:
		if not article_started:
			article_started = True
			buff = cStringIO.StringIO()
		else:
			buff.write('\t')
		buff.write(re.sub('<[^>]*>', '', line))
		counter = counter + 1
	elif article_started:
		article_started = False
		if counter > 1:
			print buff.getvalue()
		buff.close()
		buff = None
		counter = 0