import argparse
from urllib.request import urlopen
import os
import re
import time
import sys
import json


def check_url_isvalid(url):
	if(re.match(jdata['link'],url)):	
		return True
	else:
		return False

def search_links(parents,url):
	links = list()
	if("http" in url):
		try:
			sData = urlopen(url)
			sData = str(sData.read())
		
		except:
			return links
		isparent = False
		founds = [sData[m.start():m.end()] for m in re.finditer(jdata['link'], sData)]
		if(len(founds) > 0):
			for found in founds:
				### Starts with the if statement below.
				
				try:
					if(url == found):
						continue

					for p in parents:
						if(p == found or urlopen(p).read() == sData):
							isparent = True
							break
					
					if(not isparent): 
						if(sData != urlopen(found).read()):
							links.append(found)
				except:
					pass
			
					### Ends here. Will be edited later.	
	#print({url:links})
	return links				

		#print(secure_list)
		#print(insecure_list)			

def group_links(urls):
	print("Group it")

def get_domain(url):
	### Will be edited
	domain = url[url.find("/") + 2:]
	if(domain.find("/") != -1):
		domain = domain[:domain.find("/")]
	return domain

def create_string(links,args):
	if(args.all):
		print("all")
	elif(args.group):
		print("group")
	elif(args.insecure):
		print("insecure")
	elif(args.igroup):
		print("igroup")
	else:
		print("Else print")

def print_process(rec,frec):
	print("{}% completed".format((100/frec*(frec-rec))))

def recursive(links,rec,parents,frec):
	
	for i in range(len(links)):
		if(type(links[i]) == dict):
			temp = list()
			for d in links[i].keys():
				local_parents = parents.copy()
				local_parents.append(d)
				for l in range(len(links[i][d])):
					result = search_links(parents,links[i][d][l])
					if(len(result) > 0):
						temp.append({links[i][d][l]:result})
					else:
						temp.append(links[i][d][l])
				rec -= 1
				if(frec != -1):
					print_process(rec,frec)
				if(rec != 0):
					
					links[i][d] = recursive(temp,rec,local_parents,frec)
				else:
					return temp
		
	return links


def get_all_links(links, ret, isAll):
	for l in links:
		if(type(l) == dict):
			key = list(l.keys())[0]
			if(key not in ret):
				ret.append(key)
			if(isAll):
				for k in l[key]:
					if(type(k) == dict):
						ret = get_all_links([k],ret,True)
					else:
						if(k not in ret):
							ret.append(k)
		else:
			if(l not in ret):
				ret.append(l)
	return ret
			


def print_groups(links, isPrint):
	mechanisms = dict()
	for m in jdata['mechanisms']:
		mechanisms[m] = list()
	mechanisms['others'] = list()
	links = get_all_links(links, [], True)
	for l in links:
		added = False
		for m in mechanisms.keys():
			if(m in l[:7]):
				mechanisms[m].append(l)
				added = True
				break
		if(not added):
			mechanisms['others'].append(l)

	if(isPrint):
		for m in mechanisms.keys():
			if(len(mechanisms[m])>0):
				print("{} LINKS".format(m.upper()))
				print("-------------------")
				for l in mechanisms[m]:
					print(l)
				print("")
	else:
		return mechanisms

	
def print_insecure(links):
	insecure = list()
	
	for l in links:
		if(type(l) == dict):
			base_url = list(l.keys())[0]
			sub_links = get_all_links(l[base_url],[],True)
			base_url = get_domain(base_url)
			
			for s in sub_links:
				if(base_url not in s):
					insecure.append(s)
	
	if(len(insecure)> 0):
		print("FOUND POSSIBLE INSECURE LINKS")
		print("-----------------------------")
		for i in insecure:
			print(i)
	else:
		print("No insecure link found")


def print_igroup(links):
	print("Test")
def print_all(links):
	print("All")


def main():

	parser = argparse.ArgumentParser(description='''Description: Check for the Spam Link Injection. \
		Only most popular mechanisms are added.\n You can edit the settings. \
		Json file to add or delete mechanisms\n
		\nEx: python SLISearcher.py -u https://www.google.com -r -l 2 -o output.txt''')

	
	urlgroup = parser.add_mutually_exclusive_group()
	outgroup = parser.add_mutually_exclusive_group()
	securegroup = parser.add_mutually_exclusive_group()
	
	urlgroup.add_argument('-u', '--url', metavar='', help='Url to check', type=str)
	urlgroup.add_argument('-U', '--urlfile', metavar='', help='sum the integers (Default: find the max)\n\n', type=str)

	outgroup.add_argument('-a', '--all', help='Show all secure and insecure links', action='store_true')
	outgroup.add_argument('-g', '--group', help='Group by services', action='store_true')
	outgroup.add_argument('-i', '--insecure', help='Show just insecure links', action='store_true')
	outgroup.add_argument('-ig','--igroup', help='(Default Choose) - Show just insecure links grouped by services', action='store_true')
	
	securegroup.add_argument('-s','--slink', metavar='' ,help='Secure link', type=str)
	securegroup.add_argument('-S','--sfile', metavar='' ,help='Secure links file', type=str)
	
	parser.add_argument('-r','--recursive', help='Active recursive search', action='store_true')
	parser.add_argument('-l','--limit', metavar='', help='Limit resurive search deep (Default: infinite)', type=int)
	parser.add_argument('-o', '--output', metavar='', help='Output result into a file.', type=str)
	
	args = parser.parse_args()
	

	links = list()

	if(args.url):
		#print("Returned urls: " + args.url)
		if(check_url_isvalid(args.url)):
			result = search_links([],args.url)
			if(len(result) > 0):
				links.append({args.url:result})
			else:
				links.append(args.url) 
		else:
			raise Exception("Can't find a valid link")
		
			
		
		#print(parser.parse_args())
	elif(args.urlfile):
		try:
			with open(args.urlfile) as fp:
				lines = fp.readlines()
				print("Used file is: " + args.urlfile + "\n--------------" + ("-" * len(args.urlfile)) + "\n")
				for l in lines:
					if(check_url_isvalid(l)):
						secure_domains[l] = list()
						secure_domains[l].append(get_domain(l))
						result = search_links([],l)
						
						if(len(result) > 0):
							links.append({l:result})
						else:
							links.append(l)
						

		except:
			raise Exception("File is not found")
	else:
		parser.print_help()
	
	if(args.recursive):
		if(args.limit):
			links = recursive(links, args.limit,[],args.limit)
		else:
			links = recursive(links, -1, [], -1)
	#	for k in links.keys():
	#		for m in links[k].keys():
	#			if('http' in m):

	if(args.all):
		print_all(links)
	elif(args.group):
		print_groups(links, True)
	elif(args.insecure):
		print_insecure(links)
	elif(args.igroup):
		print_igroup(links)
	else:
		print(links)





if __name__ == '__main__':
	secure_list = list()
	insecure_list = list()
	with open("settings.json") as jfile:
		jdata = json.load(jfile)
	main()
	
