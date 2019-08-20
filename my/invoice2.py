# -*- coding: utf-8 -*- 
import pdfplumber
import os
import shutil
import re
import xlrd,xlwt,xlutils
from myui.invoice_translate import Ui_MainWindow
from PyQt5.QtWidgets import QApplication , QMainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(MyWindow, self).__init__(parent)
		self.setupUi(self)

def parse_pdf(path, template):
	with pdfplumber.open(path) as pdf:
		
		error = ''
		bname = os.path.basename(path)
		
		page = pdf.pages[0]
		
		text = page.extract_text()
		#print(text) 
		
		obj = re.search(r'开票日期:(.*)年(.*)月(.*)日', text)
		rq = '%s%s%s' % (obj.group(1).strip(), obj.group(2).strip(), obj.group(3).strip())
		rqs = template['rq'].split('|')
		if rq not in rqs:
			error = '%s 日期不匹配 %s' % (bname, rq)
			return error
		obj = re.search(r'(\d+)\s*发票代码', text)
		code = obj.group(1)
		obj = re.search(r'发票号码:(\d+)', text)
		num = obj.group(1)
		#print(code, num)
		
		#表格
		table = page.extract_tables()[0]
		#print(table)
		#金额
		#money = int(float(table[2][2].split('\n')[0][1:]))
		money = int(float(table[2][2].split('¥')[1]))
		
		#关键字
		words = page.extract_words()
		#print(words)
		#code = ''
		#num = ''
		#for t in words:
			#text = t['text']
			#if '发票代码' in text:
				#code = text.split(':')[1]
			#if '发票号码' in text:
				#num = text.split(':')[1]
		fname = '{}_{}-{}.pdf'.format(code, num, money) 
		#print(os.path.basename(path), fname)	

		#抬头信息列表
		tts = table[0][1].split('\n')
		#print(tts)
		
		#抬头
		tt = tts[0].split(':')[1];
		if tt != template['tt']:
			error = '{} 抬头错误'.format(bname)
			return error
		
		#税号
		sh = tts[1]
		if sh != template['sh']:
			error = '{} 税号错误'.format(bname)
			return error
		
		#地 址、电 话
		dz = tts[3].split(':')[1].strip()
		if dz:
			error = '{} 地 址、电 话错误'.format(bname)
			return error
			
		#开户行及账号
		zh = tts[4].split(':')[1]
		if zh:
			error = '{} 开户行及账号错误'.format(bname)
			return error
		
		#货物
		hw = table[1][0]
		if '移动通信设备' not in hw:
			error = '{} 货物类型错误'.format(bname)
			return error
		
		#销售方
		xsf = table[3][1]
		if template['xsf'] not in xsf:
			error = '{} 销售方错误'.format(bname)
			return error
		
		return None, fname, num, money


if __name__ == '__main__':
	
	#app = QApplication(sys.argv)
	#myWin = MyWindow()
	#myWin.show()
	#sys.exit(app.exec_())	
	
	t = {'tt':'江苏恒瑞医药股份有限公司', 'sh':'9132070070404786XB', 'xsf':'唯品会', 'rq':'20190819|20190820'}
	dir = r'C:\Users\pc\Documents\Tencent Files\249695322\FileRecv\08-19\left\65000'
	out_dir = os.path.join(dir, 'pp')
	if os.path.exists(out_dir):		
		shutil.rmtree(out_dir)
	os.makedirs(out_dir)

	book = xlwt.Workbook()            #创建excel对象
	sheet = book.add_sheet('sheet1')  #添加一个表
	row = 0
	sum = 0
	for f in os.listdir(dir):
		if f.endswith('.pdf'):
			result = parse_pdf(os.path.join(dir, f), t)
			if result[0]:
				print(result)
				continue
			sum += result[3]
			shutil.copy(os.path.join(dir, f), os.path.join(out_dir, result[1]))
			sheet.write(row, 0, result[2])
			sheet.write(row, 1, result[3])
			row += 1
	if sum > 0:
		sheet.write(row, 1, sum)
		#save
		book.save(os.path.join(out_dir, '%s.xls' % sum))
		out_dir2 = os.path.join(dir, str(sum))
		if os.path.exists(out_dir2):		
			shutil.rmtree(out_dir2)	
		os.rename(out_dir, out_dir2)		