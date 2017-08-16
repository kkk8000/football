# -*- coding:utf-8 -*-  
import httplib
import json
from sgmllib import SGMLParser
import urllib2 
from bs4 import BeautifulSoup
import gzip 
import StringIO
import copy
import codecs
import os
import csv

def dueg(t):
	try:
		return t.decode("utf-8").encode('gbk').strip()
	except:
		return t.encode('gbk').strip()

csvfile = file('football.csv', "ab")
writer = csv.writer(csvfile)
writer.writerow([dueg('轮数'), dueg('主队'), dueg('客队'), dueg('主队积分')
, dueg('客队积分'), dueg('主队排名'), dueg('客队排名')
, dueg('威廉希尔1'), dueg('威廉希尔2'), dueg('威廉希尔3')
, dueg('威廉希尔4'), dueg('威廉希尔5'), dueg('威廉希尔6')
, dueg('立博1'), dueg('立博2'), dueg('立博3')
, dueg('立博4'), dueg('立博5'), dueg('立博6')
, dueg('澳门1'), dueg('澳门2'), dueg('澳门3'), dueg('澳门4')
, dueg('澳门5'), dueg('澳门6')
, dueg('盘'), dueg('主队得分'), dueg('客队得分')
])
"""
data = [
  ('1', 'http://www.xiaoheiseo.com/', '小黑'.decode("utf-8").encode('gbk')),
  ('2', 'http://www.baidu.com/', '百度'.decode("utf-8").encode('gbk')),
  ('3', 'http://www.jd.com/', '京东'.decode("utf-8").encode('gbk'))
]
writer.writerows(data)
"""
csvfile.close()

class ListName(SGMLParser):
	def __init__(self):
		SGMLParser.__init__(self)
		self.is_h4 = ""
		self.name = []
	def start_h4(self, attrs):
		self.is_h4 = 1
	def end_h4(self):
		self.is_h4 = ""
	def handle_data(self, text):
		if self.is_h4 == 1:
			self.name.append(text)
			
stid = "&stid=9874"

for round in range(1,47):
	conn = httplib.HTTPConnection("liansai.500.com")  
	conn.request("GET", "/index.php?c=score&a=getmatch" + stid + "&round=" + str(round))  
	r1 = conn.getresponse()
	c = r1.read().decode('unicode_escape').encode("utf-8")
	ss = json.loads(c)
	#try:
	for s in ss:
		row = {}
		#print s["hsxname"]
		#print s["gsxname"]
		row = copy.deepcopy(s)
		fid = s["fid"]
		g = "http://odds.500.com/fenxi/shuju-" + str(fid) + ".shtml"
		#print g
		compresseddata = urllib2.urlopen(g).read()
		compressedstream = StringIO.StringIO(compresseddata)
		gzipper = gzip.GzipFile(fileobj=compressedstream)
		data = gzipper.read()
		soup = BeautifulSoup(data,from_encoding="gbk")
		nss = soup.find_all("div", class_="odds_nav_jfb")
		ns = nss[0]
		prevValue = ""
		nextFlag = 0
		#print ns.encode("gb2312")
		for lt in ns.strings:
			if nextFlag == 1:
				row["hjf"] = lt
				nextFlag = 0
			elif nextFlag == 2:
				row["gjf"] = lt
				nextFlag = 0
			if lt == s["hsxname"]:
				nextFlag = 1
				row["hrank"] = prevValue
			if lt == s["gsxname"]:
				nextFlag = 2
				row["grank"] = prevValue
			prevValue = lt
		
		g = "http://odds.500.com/fenxi/ouzhi-" + str(fid) + ".shtml"
		compresseddata = urllib2.urlopen(g).read()
		compressedstream = StringIO.StringIO(compresseddata)
		gzipper = gzip.GzipFile(fileobj=compressedstream)
		data = gzipper.read()
		soup = BeautifulSoup(data,from_encoding="gbk")
		#nss = soup.find_all("table", id='datatb')
		ns = soup.find("table", id='datatb')#nss[0]
		prevValue = ""
		nextFlag = 0
		row["wlxr1"] = ""
		row["wlxr2"] = ""
		row["wlxr3"] = ""
		row["wlxr4"] = ""
		row["wlxr5"] = ""
		row["wlxr6"] = ""
		t = 1
		for lt in ns.strings:
			#print type(lt)
			if lt.isspace() and nextFlag != 3:
				continue
			if nextFlag == 1:
				nextFlag = 2
			elif nextFlag == 2:
				nextFlag = 3
			elif nextFlag == 3:
				nextFlag = 4
			elif nextFlag == 4:
				try:
					f = float(lt)
					row["wlxr" + str(t)] = "" + lt.strip()
					t = t + 1
					#print lt.strip()
				except ValueError:
					nextFlag = 5
					break
			elif lt == "威廉希尔".decode("utf-8"):
				nextFlag = 1
				#print lt
		nextFlag = 0
		row["lb1"] = ""
		row["lb2"] = ""
		row["lb3"] = ""
		row["lb4"] = ""
		row["lb5"] = ""
		row["lb6"] = ""
		t = 1
		for lt in ns.strings:
			#print type(lt)
			if lt.isspace() and nextFlag != 3:
				continue
			if nextFlag == 1:
				nextFlag = 2
			elif nextFlag == 2:
				nextFlag = 3
			elif nextFlag == 3:
				nextFlag = 4
			elif nextFlag == 4:
				try:
					f = float(lt)
					row["lb" + str(t)] = "" + lt.strip()
					t = t + 1
					#print lt.strip()
				except ValueError:
					nextFlag = 5
					break
			elif lt == "立博".decode("utf-8"):
				nextFlag = 1
				#print lt
		g = "http://odds.500.com/fenxi/yazhi-" + str(fid) + ".shtml"
		compresseddata = urllib2.urlopen(g).read()
		compressedstream = StringIO.StringIO(compresseddata)
		gzipper = gzip.GzipFile(fileobj=compressedstream)
		data = gzipper.read()
		soup = BeautifulSoup(data,from_encoding="gbk")
		#nss = soup.find_all("table", id='datatb')
		ns = soup.find("table", id='datatb')#nss[0]
		prevValue = ""
		nextFlag = 0
		row["aomen1"] = ""
		row["aomen2"] = ""
		row["aomen3"] = ""
		row["aomen4"] = ""
		row["aomen5"] = ""
		row["aomen6"] = ""
		row["aomen7"] = ""
		row["aomen8"] = ""
		t = 0
		no_sj = 0
		for lt in ns.strings:
			if lt.isspace():
				continue
			if nextFlag == 1:
				nextFlag = nextFlag + 1
			elif nextFlag >= 2:
				#print nextFlag , lt.strip()
				if nextFlag == 4 and (lt.strip() != '升'.decode("utf-8") and lt.strip() != '降'.decode("utf-8")):
					no_sj = 1
				if no_sj == 0 and not (nextFlag == 6):
					if lt.strip() == '升'.decode("utf-8") or lt.strip() == '降'.decode("utf-8"):
						row["aomen" + str(t)] = row["aomen" + str(t)] + "x" + lt.strip()
					else:
						t = t + 1
						row["aomen" + str(t)] = row["aomen" + str(t)] + lt.strip()
				if no_sj == 1 and not (nextFlag == 5): 
					t = t + 1
					row["aomen" + str(t)] = row["aomen" + str(t)] + lt.strip()
				nextFlag = nextFlag + 1
				if nextFlag == 11:
					break
			elif lt == "澳门".decode("utf-8"):
				nextFlag = 1
		try:
			f = float(row["aomen6"])
		except ValueError:
			row["aomen4"] = row["aomen5"]
			row["aomen5"] = row["aomen6"]
			row["aomen6"] = row["aomen7"]
		t = 1
		try:
			csvfile = file('football.csv', "ab")
			writer = csv.writer(csvfile)
			writer.writerow([dueg(str(round)), dueg(row['hsxname']), dueg(row['gsxname'])
			, dueg(str(row['hjf'])), dueg(str(row['gjf'])), dueg(str(row['hrank'])), dueg(str(row['grank']))
			, dueg(row['wlxr1']), dueg(row['wlxr2']), dueg(row['wlxr3'])
			, dueg(row['wlxr4']), dueg(row['wlxr5']), dueg(row['wlxr6'])
			, dueg(row['lb1']), dueg(row['lb2']), dueg(row['lb3'])
			, dueg(row['lb4']), dueg(row['lb5']), dueg(row['lb6'])
			, dueg(row['aomen1']), dueg(row['aomen2']), dueg(row['aomen3']), dueg(row['aomen4'])
			, dueg(row['aomen5']), dueg(row['aomen6'])
			, dueg(row['pan']), dueg(row['hscore']), dueg(row['gscore'])
			])
			csvfile.close()
			print round,row['hsxname'],row['gsxname'],row['pan'],row['fid']
		except:
			print "\nerror",str(round),str(fid),"\n" 
			continue
		#break
	#except:
		#continue
	#break
		
	  
