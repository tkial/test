# -*- coding: utf-8 -*- 
import os

rootdir = r'C:\Users\pc\Documents\Tencent Files\249695322\FileRecv\08-19\left'
list = os.listdir(rootdir)
s = 0
for file in list:
	s += int(os.path.splitext(file)[0].split('-')[-1])
	#print os.path.splitext(file)[0].split('-')[-1]
print(s)