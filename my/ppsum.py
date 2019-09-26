# -*- coding: utf-8 -*- 
import os

rootdir = r'C:\Users\64605\Desktop\发票\08-19\400000-'
list = os.listdir(rootdir)
s = 0
for file in list:
	s += int(os.path.splitext(file)[0].split('-')[-1])
	#print os.path.splitext(file)[0].split('-')[-1]
print(s)