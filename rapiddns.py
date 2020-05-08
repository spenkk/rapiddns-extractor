import os, requests, sys, csv, colorama
from colorama import Fore, Style
from bs4 import BeautifulSoup

if len(sys.argv)<2:
	print("Usage: python " + sys.argv[0] + " target.com")
	sys.exit(1)

def onlysubdomains():
	with open("all.txt") as lines:
		for i in lines:
			url = i.split(",")[0]
			domain = url.split("//")[-1].split("/")[0]
			
			with open ('domains-temp.txt', 'a') as temp:
					temp.write(domain + '\n')

		# Sorting and removing duplicates
		lines_seen = set()
		outfile = open('subdomains.txt', 'w')
		for line in open('domains-temp.txt', 'r'):
			if line not in lines_seen:
				if not line.strip(): continue
				outfile.write(line)
				lines_seen.add(line)
				print(Fore.GREEN + '' + line.rstrip() + '' + Style.RESET_ALL)
		outfile.close()
		os.remove('domains-temp.txt')

def withDescription():
	for website_name in website_table_items:
		web = website_name.contents[-1].strip()
		urls = website_name['href'] + ', "' + web + '"' 
		with open('all.txt', 'a') as out:
			out.write(urls + '\n')



url = "https://rapiddns.io/subdomain/{}?full=1#result".format(sys.argv[1])

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

output_rows = []
website_table = soup.find("table",{"class":"table table-striped table-bordered"})
website_table_items = website_table.find_all('a', href=True)


if __name__ == "__main__":
	
	withDescription()
	onlysubdomains()
