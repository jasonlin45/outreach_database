import bs4
import csv

from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

	
	
if __name__ == "__main__":		
	
	#TODO: Adapt to new format
	def write_file(dict, fileName):
		with open(fileName, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			#csvWriterDumb = [names[0][i]] + [names[1][i]] + [names[2][i]] + [names[3][i]]
			#writer.writerow(csvWriterDumb)
			for key, value in dict.items():
				toArr = [key] + [value]
				print(key, ':', value, "\n")
				writer.writerow(toArr)
	
	dictionary = {}

	my_url = 'http://2017.igem.org/Team:MIT/outreach'
	uClient = uReq(my_url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "lxml")
	
	style_tags = page_soup.find_all("style")
	for style in style_tags:
		style.extract()
	#print(style_tag)
	
	content = page_soup.find_all("body")[0]
	headings = content.find_all(["h1","h2","h3","h4","h5"])
	#print(headings)
	print (len(headings))
	for heading in headings:
		heading_text = heading.get_text()
		next_tag = heading.find_next_sibling(["p","p1","p2"])
		#print (countFreq("{", a))
		if next_tag != None:
			dictionary[heading_text] = next_tag.get_text()
			print("/////////////////////////")
			print (heading_text + "\n")
			print (next_tag.get_text())
	print(dictionary)
	
	write_file(dictionary, "MIT.csv")
		
		
		