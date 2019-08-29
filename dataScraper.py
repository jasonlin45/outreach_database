import bs4
import csv

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
					toArr = [key] + [key2] + [val2]
					print(key2, ':', val2, "\n")
					writer.writerow(toArr)
	
	bigDict = {}
	contentDictionary = {}
	
	site_name = "MIT"
	my_url = 'http://2017.igem.org/Team:MIT/HP/Gold_Integrated'
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "lxml")
	
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
		
	bigDict[site_name] = dict(contentDictionary)
	print(bigDict)
	write_file(bigDict, "MIT.csv")
		
		
		