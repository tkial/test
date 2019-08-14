# -*- coding: utf-8 -*- 
import os

rootdir = 'C:\\Users\\pc\\Desktop\\3w\\7-24\\all'
list = os.listdir(rootdir)
s = 0
for file in list:
	s += int(os.path.splitext(file)[0].split('-')[-1])
	#print os.path.splitext(file)[0].split('-')[-1]
print(s)