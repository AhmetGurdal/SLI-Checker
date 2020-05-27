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

	return links				

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
			
def create_output(links, isPrint):
	print(links)
	with open(isPrint, "w") as f:
		for l in links:
			f.write(l)
			f.write("\n")
	print("{} file is created.".format(isPrint))
		

def print_groups(links, isPrint):
	mechanisms = dict()
	for m in jdata['mechanisms']:
		mechanisms[m] = list()
	mechanisms['others'] = list()
	if(type(links) == dict):
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
		output = list()
		for m in mechanisms.keys():
			if(len(mechanisms[m])>0):
				output.append("{} LINKS".format(m.upper()))
				output.append("-------------------")
				for l in mechanisms[m]:
					output.append(l)
				output.append("")

		create_output(output,isPrint)

	else:
		for m in mechanisms.keys():
			if(len(mechanisms[m])>0):
				print("{} LINKS".format(m.upper()))
				print("-------------------")
				for l in mechanisms[m]:
					print(l)
				print("")

	
def print_insecure(links,isPrint, isReturn):
	insecure = list()
	
	for l in links:
		if(type(l) == dict):
			base_url = list(l.keys())[0]
			sub_links = get_all_links(l[base_url],[],True)
			secure_list[base_url].append(get_domain(base_url))
			length = len(base_url) + 3
			for l in sub_links:
				isSecure = False
				for s in secure_list[base_url]:
					if(s in l[:length]):
						isSecure = True
				if(not isSecure):
					insecure.append(l)
					
	if(isPrint):
		insecure.insert(0,"-----------------------------")
		insecure.insert(0,"FOUND POSSIBLE INSECURE LINKS")
		create_output(insecure,isPrint)
	if(isReturn):
		return insecure

	else:
		if(len(insecure)> 0):
			
			print("FOUND POSSIBLE INSECURE LINKS")
			print("-----------------------------")
			for i in insecure:
				print(i)
		else:
			print("No insecure link found")


def print_igroup(links, isPrint):
	links = print_insecure(links,False,True)
	print_groups(links,isPrint)
		


def print_all(links, isPrint):
	links = get_all_links(links,[],True)
	if(isPrint):
		links.insert(0,"-----------")
		links.insert(0,"FOUND LINKS")
		create_output(links,isPrint)
	else:
		print("FOUND LINKS")
		print("-----------")
		for l in links:
			print(l)





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
	


	
	if(len(secure_list) > 0):
		print("SECURE LIST")
		print("-----------")
		for s in secure_list:
			print(s)
		print("-----------")

	print("Process is started...")


	links = list()

	if(args.url):
		#print("Returned urls: " + args.url)
		if(check_url_isvalid(args.url)):
			secure_list[args.url] = list()

			if(args.slink):
				secure_list[args.url].append(args.slink)
			
			elif(args.sfile):
				with open(args.sfile) as fp:
					lines = fp.readlines()
					for l in lines:
						l = l.replace(" ", "")
						base = l[:l.find("::")]
						if(base in args.url):
							
							for s in l[l.find("::") + 2 : ].split("|"): 
								if("\n" in s):
									secure_list[base].append(s[:-1])
								else:
									secure_list[base].append(s)

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
					print(l)
					if(check_url_isvalid(l)):
						secure_list[l] = list()
						if(args.slink):
							secure_list[l].append(args.slink)

						elif(args.sfile):
							with open(args.sfile) as fp:
								lines = fp.readlines()
								for line in lines:
									line = line.replace(" ", "")
									base = line[:line.find("::")]
									if(base in l):
										for s in line[line.find("::") + 2 : ].split("|"):
											if("\n" in s):
												secure_list[base].append(s[:-1])
											else:
												secure_list[base].append(s)


						print("Process")
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

	

	if(args.all):
		print_all(links, args.output)
	elif(args.group):
		print_groups(links, args.output)
	elif(args.insecure):
		print_insecure(links, args.output, False)
	elif(args.igroup):
		print_igroup(links, args.output)
	else:
		if(args.output):
			create_output(get_all_links(links,[],True),args.output)
		else:
			print(links)


if __name__ == '__main__':
	secure_list = dict()
	insecure_list = list()
	with open("settings.json") as jfile:
		jdata = json.load(jfile)
	main()
	
