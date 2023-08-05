'''
Author: Krishna
MailID: kvrks@outlook.com
'''

import os, fnmatch, time
from datetime import datetime
'''
	 B : Byte, KB : Kilobyte, MB : Megabyte, GB : Gigabyte, TB : Terabyte, 
	 PB : Petabyte, EB : Exabyte, ZB : Zettabyte, YB : Yottabyte
'''
def frombytes(size_in_bytes):
	size = size_in_bytes
	size_unit_list = [' B', ' KB', ' MB', ' GB', ' TB', ' PB', ' EB', ' ZB', ' YB']
	size_unit_iter = iter(size_unit_list)
	size_unit = next(size_unit_iter)
	while size > 1024.0:
		try:
			size_unit = next(size_unit_iter)
			size /= 1024.0
		except StopIteration:
			break
	return str(round(size,2))+size_unit

def tobytes(size_in_str):
	size = float(size_in_str[:size_in_str.index(' ')])
	size_unit_list = [' YB', ' ZB', ' EB', ' PB', ' TB', ' GB', ' MB', ' KB', ' B']
	size_unit_iter = iter(size_unit_list)
	size_unit = next(size_unit_iter)
	while size_unit not in size_in_str:
		size_unit = next(size_unit_iter)
	while True:
		try:
			size_unit = next(size_unit_iter)
			size *= 1024.0
		except StopIteration:
			break
	return size
	
def getdict(files_info_list):
	files_info_dict = dict()
	for f in files_info_list:
		files_info_dict[f['path']+f['time'].strftime('_%d%m%Y%H%M%S')]=f
	return files_info_dict
		
def sortfilesby(files_info_list, key, order):
	reverseoption = False
	if order=='desc':
		reverseoption = True
	if key=='time':
		return files_info_list.sort(key=lambda dic: dic['time'], reverse=reverseoption)
	if key=='size':
		return files_info_list.sort(key=lambda dic: tobytes(dic['size']), reverse=reverseoption)
	else:
		return files_info_list.sort(key=lambda dic: dic[key], reverse=reverseoption)
		
def descendants(parent, recursive):
	for descendant in os.scandir(parent):
		yield descendant
		if descendant.is_dir() and not descendant.is_symlink():
			yield from descendants(descendant.path, recursive)
				
def glob(directory, filemask, recursive, watch):
	for item in descendants(directory,recursive):
		if fnmatch.filter([item.path],filemask):
			if item.is_file():
				try:
					itemstat = item.stat()
					item_info = {'name': item.name, 'path': item.path, 'time': datetime.fromtimestamp(itemstat.st_mtime), 'size': frombytes(itemstat.st_size), 'status': 'Extraction successful'}
				except Exception as e:
					itemstat = item.stat()
					item_info = {'name': item.name, 'path': item.path, 'time': datetime.fromtimestamp(itemstat.st_mtime), 'size': frombytes(itemstat.st_size), 'stat': 'Extraction failed due to '+repr(e)}
				if watch:
					print(item_info)
				yield item_info
