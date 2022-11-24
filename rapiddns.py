import os, requests, sys, csv, colorama
from colorama import Fore, Style
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

if len(sys.argv)<2:
	print("Usage: python " + sys.argv[0] + " target.com")
	sys.exit(1)


url = "https://rapiddns.io/subdomain/{}?full=1#result".format(sys.argv[1])

page = requests.get(url, verify=False)
soup = BeautifulSoup(page.text, 'html.parser')

output_rows = []
website_table = soup.find("table",{"class":"table table-striped table-bordered"})
website_table_items = website_table.find_all('tbody')
for tbody in website_table_items:
	tr = tbody.find_all('tr')
	for td in tr:
		subdomain = td.find_all('td')[0].text

		# Sorting and removing duplicates			
		with open ('domains-temp.txt', 'a') as temp:
			temp.write(subdomain + '\n')

	lines_seen = set()
	outfile = open('{}-rapiddns.out'.format(sys.argv[1]), 'w')
	for line in open('domains-temp.txt', 'r'):
		if line not in lines_seen:
			if not line.strip(): continue
			outfile.write(line)
			lines_seen.add(line)
			print(Fore.GREEN + '' + line.rstrip() + '' + Style.RESET_ALL)
	outfile.close()
	os.remove('domains-temp.txt')
