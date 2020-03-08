from bs4 import BeautifulSoup as Soup


class IED:
	"""
	Class IED represents a single device in the SCD file
	"""

	def __init__(self):
		"""dict with a extracted values"""
		self.values = {}
		self.xml = None

	def print_all(self):
		"""Print all prints all the function from the values dictionary"""
		print(self.values)

	def load_IED_section(self, xml):
		"""
		Load IED get the XML from the BS4

		:param xml: the fragment from the SCD file that represents single IED
		:return:
		"""
		self.xml = xml

	def extract(self):
		"""
		Extract method extracts all the relevant information from the xml fragment passed in the load_IED_section.
		If the dataset is Static, then the dataset information is extracted (specific signals in the datasets)
		:return: loads into the self.values dict
		"""
		self.values['name'] = self.xml['name']
		self.values['typeIED'] = self.xml['type']
		self.values['manufacturer'] = self.xml['manufacturer']
		# check if there is description supplied
		if self.xml.has_attr('desc'):
			self.values['desc'] = self.xml['desc']
		# check if there is configVersion supplied
		if self.xml.has_attr('configVersion'):
			self.values['configVers'] = self.xml['configVersion']
		datasets = self.xml.findAll('DataSet')
		if datasets:
			self.values['DataSets_Type'] = "Static"
			self.extract_dataset_information()
		else:
			self.values['DataSets_Type'] = "Dynamic"

	def extract_dataset_information(self):
		"""
		Function finds all dataset infromation in the xml IED sections and creates additional dictionaries
		"""
		datasets = self.xml.findAll('DataSet')
		self.values['Dataset_Data'] = {}
		list_of_signals = {}
		for dataset in datasets:
			#check the name of dataset
			datasetname = dataset['name']
			#find all signals in the data
			results = dataset.findAll('FCDA')
			for signal in results:
				#create an dictionary with signal names and empty strings for descriptions
				list_of_signals[signal['doName']] = ""
				#find all DOI elements (holding desc for signal)
				dois = self.xml.findAll('DOI')
				for signal in list_of_signals:
					for doi in dois:
						if doi['name'] == signal:
							desc = doi['desc']
							list_of_signals[signal] = desc
							break
			#fill the dataset_data with the signals that are in the datasets
			self.values['Dataset_Data'][datasetname] = ""
			self.values['Dataset_Data'][datasetname] =	list_of_signals


# TODO
# better printing
