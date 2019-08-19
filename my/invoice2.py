# -*- coding: utf-8 -*- 
import pdfplumber
import os
import shutil
import re
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
		if not template['rq'] == rq:
			error = '%s 日期不匹配 %s' % (bname, rq)
			return None, None, error
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
			return None, None, error
		
		#税号
		sh = tts[1]
		if sh != template['sh']:
			error = '{} 税号错误'.format(bname)
			return None, None, error
		
		#地 址、电 话
		dz = tts[3].split(':')[1].strip()
		if dz:
			error = '{} 地 址、电 话错误'.format(bname)
			return None, None, error
			
		#开户行及账号
		zh = tts[4].split(':')[1]
		if zh:
			error = '{} 开户行及账号错误'.format(bname)
			return None, None, error
		
		#货物
		hw = table[1][0]
		if '移动通信设备' not in hw:
			error = '{} 货物类型错误'.format(bname)
			return None, None, error
		
		#销售方
		xsf = table[3][1]
		if template['xsf'] not in xsf:
			error = '{} 销售方错误'.format(bname)
			return None, None, error
		
		return fname, money, error

if __name__ == '__main__':
	
	#app = QApplication(sys.argv)
	#myWin = MyWindow()
	#myWin.show()
	#sys.exit(app.exec_())	
	
	t = {'tt':'江苏恒瑞医药股份有限公司', 'sh':'9132070070404786XB', 'xsf':'唯品会', 'rq':'20190819'}
	dir = r'C:\Users\64605\Desktop\发票\08-19\400000-'
	out_dir = os.path.join(dir, 'pp')
	if os.path.exists(out_dir):		
		shutil.rmtree(out_dir)
	os.makedirs(out_dir)
	sum = 0
	for f in os.listdir(dir):
		if f.endswith('.pdf'):
			fname, money, error = parse_pdf(os.path.join(dir, f), t)
			if error:
				print(error)
				continue
			sum += money
			shutil.copy(os.path.join(dir, f), os.path.join(out_dir, fname))
	out_dir2 = os.path.join(dir, str(sum))
	if os.path.exists(out_dir2):		
		shutil.rmtree(out_dir2)	
	os.rename(out_dir, out_dir2)		