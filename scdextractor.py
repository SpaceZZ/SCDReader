import sys
from bs4 import BeautifulSoup as Soup

from model.IED import IED
from model.scd import ScdMetaInfo


def parse_file(file):
	"""
	Function reads the .SCD file into the Beautiful Soup soup

	:param file: uri to the .SCD file
	:return: the BS4 processed xml
	"""

	try:
		if file is None:
			file = sys.argv[1]
		if file.endswith('.scd') or file.endswith('.icd'):
			handler = open(file).read()
			soup = Soup(handler, "xml")
			return soup
		else:
			raise ValueError('File is not .scd or .icd file')
	except:
		raise Exception


# noinspection PyShadowingNames
def extract_IEDs(scd):
	"""
	Function extracts single IED xml paragraph from the soup

	:param scd: the BS4 object
	:return: returns the list with the extracted IEDs
	"""

	# extract all information about the IEDs
	IEDs = scd.findAll("IED")
	extracted_devices = []
	for section in IEDs:
		# create new IED object
		item = IED()
		# load IED xml section
		item.load_IED_section(section)
		# extract the relevant information
		item.extract()
		# add to the extracted devices list
		extracted_devices.append(item)
	return extracted_devices


def extract_IP(scd, extracted_IEDs):
	"""
	Function extracts the IP addresses from the .SCD based on the found IED names and assigns them to the IEDs

	:param scd: the whole parsed scd file
	:param extracted_IEDs: the list of all previously extracted IEDs
	:return: IEDs list with completed IP addressing
	"""

	for device in extracted_IEDs:
		comm_section = scd.find(attrs={"iedName": device.values['name']})
		device.values['Port'] = comm_section['apName']
		device.values['IP'] = comm_section.find(attrs={'type': "IP"}).text
		device.values['IP-SUBNET'] = comm_section.find(attrs={'type': "IP-SUBNET"}).text
		device.values['IP-GATEWAY'] = comm_section.find(attrs={'type': "IP-GATEWAY"}).text

	return extracted_IEDs


def extract_meta_information(scd):
	"""
	Function extracts meta information from the file

	:param scd: accepts the scd soup raw input
	:return: fully configured scd_file object
	"""

	scd_meta_info = ScdMetaInfo()

	header_section = scd.find('Header')

	scd_meta_info.values['id'] = header_section['id']
	scd_meta_info.values['version'] = header_section['version']
	scd_meta_info.values['revision'] = header_section['revision']
	scd_meta_info.values['toolID'] = header_section['toolID']
	# find last HistoryItem in the Header Section
	last_history_item = header_section.findAll('Hitem')[-1]
	scd_meta_info.values['updated'] = last_history_item['when']
	scd_meta_info.values['who'] = last_history_item['who']

	return scd_meta_info
