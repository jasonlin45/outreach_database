import bs4
import csv
import json

# Imports for selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs
import pandas as pd
import re
import os

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

if __name__ == "__main__":
	
	def write_file(dict, fileName):
		with open("Data/"+fileName, 'w', newline='', encoding = 'utf-8-sig') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			#csvWriterDumb = [names[0][i]] + [names[1][i]] + [names[2][i]] + [names[3][i]]
			#writer.writerow(csvWriterDumb)
			for key, value in dict.items():
				for key2, val2 in value.items():
					for key3, val3, in val2.items():
						toArr = [key] + [key2] + [key3] + [val3]
						print(key3, ':', val3, "\n")
						writer.writerow(toArr)

	# Create headless chrome
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"

	driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), chrome_options=chrome_options)
	bigDict = {}
	pageDict = {}
	contentDictionary = {}
	# Open section data
	with open("testScrape.csv", "r") as read_file:
		csv_reader = csv.DictReader(read_file)
		for row in csv_reader:
			print(row['team_name'], row['wiki_link'])
			base_url = row['wiki_link']
			driver.get(base_url)
			driver.implicitly_wait(1)
			soup = bs(driver.page_source, "lxml")
			# Find human practices pages
			# They can call it a variety of things
			# Search on a keyword list
			# [link, link_text, link, link_text,...]
			links = []
			#keywordsList = ["human", "practices", "integrated", "education", "public", "engagement"]
			keywordsList = ["uman", "ractices", "ntegrated", "ducation", "ublic", "ngagement", "UMAN", "RACTICES", "NTEGRATED", "DUCATION", "UBLIC", "NGAGEMENT"]
			for keyword in keywordsList:
				#elementsList = driver.find_elements_by_xpath("//a[contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'),"+keyword+")]")
				elementsList = soup.find_all("a", string=re.compile(keyword))
				#print(elementsList)
				for element in elementsList:
					link = element.get("href")
					text = element.text.strip()
					if link not in links and "http" in link:
						#print(link)
						links.append(link)
						links.append(text)
					
			
			for i in range(0,len(links),2):
				link = links[i]
				page_title = links[i+1]
				driver.get(link)
				page_soup = bs(driver.page_source, "lxml")
				site_name = row['team_name']
				style_tags = page_soup.find_all("style")
				for style in style_tags:
					style.extract()
				
				content = page_soup.find_all("body")[0]
				
				
				
				
				style_tags = page_soup.find_all("style")
				for style in style_tags:
					style.extract()
				#print(style_tag)
				
				content = page_soup.find_all("body")[0]
				hTags = ["h1","h2","h3","h4","h5"]
				pTags = ["p", "p1", "p2"]
				headings = content.find_all(hTags)
				
				#print(headings)
				print (len(headings))
				for heading in headings:
					heading_text = heading.get_text()
					next_tag = heading.next_sibling
					print(next_tag)
					next_text = ""
					while next_tag != None and next_tag.name not in hTags:
						if(next_tag.string!=None) and next_tag.name in pTags:
							next_text += next_tag.string
						next_tag = next_tag.next_sibling
					#print (countFreq("{", a))
					# if next_tag != None:
						# contentDictionary[heading_text] = next_tag.get_text()
						# print("/////////////////////////")
						# print (heading_text + "\n")
						# print (next_tag.get_text())
					if next_text != "":
						contentDictionary[heading_text] = next_text
				pageDict[page_title] = dict(contentDictionary)	
			bigDict[site_name] = dict(pageDict)
			print(content)
	
	print(bigDict)
	write_file(bigDict, "initial_data.csv")
	




# if __name__ == "__main__":		
	
# 	def write_file(dict, fileName):
# 		with open("Data/"+fileName, 'w', newline='', encoding = 'utf-8-sig') as csvfile:
# 			writer = csv.writer(csvfile, delimiter=',')
# 			#csvWriterDumb = [names[0][i]] + [names[1][i]] + [names[2][i]] + [names[3][i]]
# 			#writer.writerow(csvWriterDumb)
# 			for key, value in dict.items():
# 				for key2, val2 in value.items():
# 					toArr = [key] + [key2] + [val2]
# 					print(key2, ':', val2, "\n")
# 					writer.writerow(toArr)
	
# 	bigDict = {}
# 	contentDictionary = {}
	
# 	site_name = "MIT"
# 	my_url = 'http://2017.igem.org/Team:MIT/HP/Gold_Integrated'
# 	uClient = uReq(my_url)
# 	page_html = uClient.read()
# 	uClient.close()
# 	page_soup = soup(page_html, "lxml")
	
# 	style_tags = page_soup.find_all("style")
# 	for style in style_tags:
# 		style.extract()
# 	#print(style_tag)
	
# 	content = page_soup.find_all("body")[0]
# 	hTags = ["h1","h2","h3","h4","h5"]
# 	pTags = ["p", "p1", "p2"]
# 	headings = content.find_all(hTags)
	
# 	#print(headings)
# 	print (len(headings))
# 	for heading in headings:
# 		heading_text = heading.get_text()
# 		next_tag = heading.next_sibling
# 		print(next_tag)
# 		next_text = ""
# 		while next_tag != None and next_tag.name not in hTags:
# 			if(next_tag.string!=None) and next_tag.name in pTags:
# 				next_text += next_tag.string
# 			next_tag = next_tag.next_sibling
# 		#print (countFreq("{", a))
# 		# if next_tag != None:
# 			# contentDictionary[heading_text] = next_tag.get_text()
# 			# print("/////////////////////////")
# 			# print (heading_text + "\n")
# 			# print (next_tag.get_text())
# 		if next_text != "":
# 			contentDictionary[heading_text] = next_text
		
# 	bigDict[site_name] = dict(contentDictionary)
# 	print(bigDict)
# 	write_file(bigDict, "MIT.csv")

		
		