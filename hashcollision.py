#!/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import base64
from optparse import OptionParser

class Permutation():
	def __init__(self, arr, mode):
		self.arr = arr
		if(mode !=1 and mode !=2):
			print 'You must input the right mode : '
			print '	1--fast mode'
			print '	2--slow mode'
			exit(0)
		self.mode = mode
		self.result = []
		self.split_str = []
		self.split_str_normal = ['', ' ', '_', '|',  ":"]
		self.split_str_large = ['',' ','`','~','!','@','#','$','%','^','&','*',"-",'_','+','=','|',";",":",'{}','[]','()']

	def swap(self, i, j):
		temp = self.arr[i]
		self.arr[i] = self.arr[j]
		self.arr[j] = temp

	def addSplitStr(self, arr, flag, mode):
		if(mode == 1):
			self.split_str = self.split_str_normal
		else:
			self.split_str = self.split_str_large

		if(flag):
			self.split_str = arr
		else:
			self.split_str.extend(arr)

	def arrange(self, start, end):
		if(start==end):
			self.result.append(tuple(self.arr))
		else:
			for i in range(start, end):
				self.swap(start, i)
				self.arrange(start+1,end)
				self.swap(i,start)
		return self.result

	def Combination(self):
		temp = []
		result = self.arrange(0, len(self.arr))
		for i in range(len(self.arr)):
			for j in range(len(result)):
				res = result[j][0:i+1]
				if res not in temp:
					temp.append(res) 
		return temp


	def processList(self, arr, mode):
		result = []
		special = []
		if(mode == 1):
			special = {'(': ')', '{': '}'}
		elif(mode == 2):
			special = {'<': '>', '{': '}', '[': ']', '(': ')', '"': '"', "'": "'"}

		for i in self.split_str:
			result.append(i.join(arr))

			for key,value in special.iteritems():
				temp = []
				for j in range(len(arr)):
					temp.append((str(key) + arr[j] + str(value)))
				result.append(i.join(temp))
		return result

	def getResult(self):
		temp = []
		result = self.Combination()
		for i in result:
			temp.extend(self.processList(i, self.mode))
		return temp

def mysql_old_hash(str):
	nr = 1345345333  
	add = 7  
	nr2 = 0x12345671  
	for c in (ord(x) for x in str if x not in (' ', '\t')):  
		nr^= (((nr & 63)+add)*c)+ (nr << 8) & 0xFFFFFFFF  
		nr2= (nr2 + ((nr2 << 8) ^ nr)) & 0xFFFFFFFF  
		add= (add + c) & 0xFFFFFFFF  
	return "%08x%08x" % (nr & 0x7FFFFFFF, nr2 & 0x7FFFFFFF)

def mysql_new_hash(str):  
	pass1 = hashlib.sha1(str).digest()
	pass2 = hashlib.sha1(pass1).hexdigest()
	return pass2.upper()

def getHashes(arr):
	temp = {}
	for i in arr:
		md5Hash = hashlib.md5(i).hexdigest()
		md5Md5Hash = hashlib.md5(md5Hash).hexdigest()
		sha1Hash = hashlib.sha1(i).hexdigest()
		sha256Hash = hashlib.sha256(i).hexdigest()
		sha384Hash = hashlib.sha384(i).hexdigest()
		sha512Hash = hashlib.sha512(i).hexdigest()
		b64str = base64.b64encode(i)

		str = 'md5(' + i + ')'
		temp[str] = md5Hash
		str = 'md5(md5(' + i + '))'
		temp[str] = md5Md5Hash
		str = 'md5(md5(md5(' + i + ')))'
		temp[str] = hashlib.md5(md5Md5Hash).hexdigest()
		str = 'md5(base64(' + i + '))'
		temp[str] = hashlib.md5(b64str).hexdigest()
		str = 'mysql(' + i + ')'
		temp[str] = mysql_old_hash(i)
		str = 'mysql5(' + i + ')'
		temp[str] = mysql_new_hash(i)
		str = 'sha1(' + i + ')'
		temp[str] = sha1Hash
		str = 'sha1(sha1(' + i + '))'
		temp[str] = hashlib.sha1(sha1Hash).hexdigest()
		str = 'md5(sha1(' + i + '))'
		temp[str] = hashlib.md5(sha1Hash).hexdigest()
		str = 'sha1(md5(' + i + '))'
		temp[str] = hashlib.sha1(md5Hash).hexdigest()
		str = 'sha256(' + i + ')'
		temp[str] = sha256Hash
		str = 'sha384(' + i + ')'
		temp[str] = sha384Hash
		str = 'sha512(' + i + ')'
		temp[str] = sha512Hash
	return temp


if __name__ == '__main__':
	parser = OptionParser('%prog -p <params> --hash <hash>')
	parser.add_option('-p', dest='params', type='string', help='specify the params to generate hash, separated by comma')
	parser.add_option('--hash', dest='hash', type='string', help='the target hash to collision')
	parser.add_option('--extra', dest='extra', type='string',help='manually specify extra separators, separated by comma')
	parser.add_option('--extraonly', dest='extraonly', action='store_true', help='tell program to use manually separators only')
	parser.add_option("--mode", dest='mode', type='int', help='specify the running mode\r\n\t0--default mode\r\n\t1--detailed mode\r\n\t2--comprehensive mode')
	parser.add_option('-v','--verbose', dest='verbose', type='int', help="specify the verbosity level, default is 0, chose")

	(options, args) = parser.parse_args()
	if(options.hash == None):
		print 'You must specify a target hash to collision...'
		exit(0)
	if(options.params == None):
		print 'You must specify params to generate hash...'
		exit(0)

	res = None
	try:
		if(options.extra != None):
			if(options.extraonly != None):
				options.extraonly = True
				print '[!] You are chosing extraonly mode...'
			else:
				options.extraonly = False

		if (options.mode == None or options.mode == 1):
			options.mode = 1
			if options.extraonly == False:
				print '[!] You are chosing fast mode...'
		else:
			if options.extraonly == False:
				print '[!] You are chosing slow mode...'
		res = Permutation(options.params.split(','), options.mode)
		res.addSplitStr(options.extra.split(','), options.extraonly, options.mode)
	except:
		print 'You didn\'t input all the parameters correctly'
		exit(0)

	payloads = res.getResult()
	hashes = getHashes(payloads)
	if(options.verbose == None):
		options.verbose = 0
	elif(options.verbose == 1 or options.verbose == 2):
		pass
	else:
		print 'You didn\'t input the right verbosity level :'
		print '	0--default mode'
		print '	1--detailed mode'
		print '	2--comprehensive mode'
		exit(0)
	print '[!] Collision is about to start, please fasten your seat belts!'
	if(options.verbose == 0):
		for key, value in hashes.iteritems():
			if(value.lower() == options.hash.lower()):
				print "[+] Collision Success!"
				print '[+]', key, ':', value
				exit(0)
		print '[-] Collision Failed!'
		print '[-] There are ' + str(len(hashes)) + ' collosiones happened, but we didn\'t found the hash you want!'
	if(options.verbose == 1):
		for key, value in hashes.iteritems():
			print '[!] Testing', value
			if (value.lower() == options.hash.lower()):
				print "[+] Collision Success!"
				print '[+]', key, ':', value
				exit(0)
		print '[-] Collision Failed!'
		print '[-] There are ' + str(len(hashes)) + ' collosiones happened, but we didn\'t found the hash you want!'
	if (options.verbose == 2):
		for key, value in hashes.iteritems():
			print '[!] Testing',key,':',value
			if (value.lower() == options.hash.lower()):
				print ''
				print "[+] Collision Success!"
				print '[+]', key, ':', value
				exit(0)
		print ''
		print '[-] Collision Failed!'
		print '[-] There are ' + str(len(hashes)) + ' collosiones happened, but we didn\'t found the hash you want!'