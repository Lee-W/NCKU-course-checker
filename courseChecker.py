# -*- coding: utf-8 -*-  

import urllib  
import HTMLParser  
import sys

added = False
formStart = False
columnStart = False
result = [] 
course = []

title = [ "系所名稱" , "系號" , "序號" , "課程碼" ,
	  "分班碼" , "班別" , "年級" , "類別" ,
	  "英語授課" , "課程名稱" , "選必修" , "學分" ,
	  "教師姓名" , "已選課人數 " , "餘額 " , "時間" ,
	  "教室" , "備註" , "限選條件" , "業界專家參與" , "屬性碼" , "跨領域學分學程" ] 

class courseHTMLParser(HTMLParser.HTMLParser):  

	def handle_starttag(self, tag, attrs): 
		global  added , course , formStart ,columnStart

		if tag == 'tr':
			formStart = True
			course = []
		if tag == 'td' :
			columnStart = True
			added = False
	
	def handle_data(self, data):
		global added , course, formStart ,columnStart
		
		if formStart == True:
			if data.strip() == "":
				added = True
				course.append(u' ')
			else:
				if added ==True and columnStart == True:
					course[ len(course)-1 ] += " " + data.strip()
				else:	
					added = True
					course.append( data.strip() )
	
	def handle_endtag(self, tag): 
		global added , course , formStart ,columnStart , result

		if tag == 'tr':
			formStart = False
			result.append(course)
		if tag == 'td':
			column = False
			if added == False:
				course.append(u' ')
  
	
	def unknown_decl(self, data):
		"""Override unknown handle method to avoid exception"""  
        pass  

def mainProcess( dNo ): 

	courseWeb = urllib.urlopen("http://140.116.165.74/qry/qry001.php?dept_no="+dNo)  
	webContent = courseWeb.read().decode('utf_8')  
	courseWeb.close()  
	Parser = courseHTMLParser()  
  
	try:  
		for line in webContent.splitlines():  
			if hasattr(Parser, 'stop') and Parser.stop:  
				break  
			Parser.feed(line)  
	except HTMLParser.HTMLParseError, data:  
		print "# Parser error : " + data.msg  
  
	Parser.close()  

	result[0] = title

	printList=[1,2,9,10,11,12,13,14,15]

	for i in range ( 0 , len(result) ):
		for j in range ( 0 , len(result[i]) ):
			for k in range ( 0 , len(printList) ):
				if j is not printList[k]:
					continue			
	
				if i is 0:
					print result[i][j]+"\t",
					if j is printList[len(printList)-1]:
						print "\n",

				elif result[i][14].find(u'\u6eff') is -1 :
					if j is 9:
						print "%7s\t" %result[i][j][0:min(7,len(result[i][j]))],
						continue
					if j is 12:
						if len (result[i][j]) > 3:
							print "%3s*\t\t" %result[i][j][0:3],
						else:
							print "%3s\t\t" %result[i][j],
						continue
					if j is 14:
					 	print "\t",

					print result[i][j]+"\t",

					if j is printList[len(printList)-1]:
						print "\n",
			



departmentNo = raw_input('請輸入系所代碼:')

while( departmentNo!= "bye" ):
	mainProcess( departmentNo )
	added = False
	formStart = False
	columnStart = False
	result = [] 
	course = []
	departmentNo = raw_input('\n如果完成了請輸入bye\n請輸入系所代碼:')
