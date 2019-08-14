# -*- coding: utf-8 -*- 
import pdfplumber
import os
import shutil
import myui.invoice_translate
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
		
		#表格
		table = page.extract_tables()[0]
		#金额
		money = int(float(table[2][2].split('\n')[0][1:]))
		
		#关键字
		words = page.extract_words()
		code = ''
		num = ''
		for t in words:
			text = t['text']
			if '发票代码' in text:
				code = text.split(':')[1]
			if '发票号码' in text:
				num = text.split(':')[1]
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
		dz = tts[3].split(':')[1]
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
	
	app = QApplication(sys.argv)
		myWin = MyWindow()
		myWin.show()
		sys.exit(app.exec_())	
	
	t = {'tt':'江苏豪森药业集团有限公司', 'sh':'913207006083959289', 'xsf':'苏宁易购'}
	dir = r'C:\Users\64605\Desktop\发票\q-203239'
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