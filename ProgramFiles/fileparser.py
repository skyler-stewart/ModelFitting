'''
fileParser.py 
Includes functions for parsing data from datafiles and parsing settings from settings.ini. 
'''

# Imports #
import sys
import configparser
import json
from pathlib import Path
from datetime import date

from models import * 

# Globals # 
today = date.today() 

# Filepaths 
global programFolder
global dataFolder 
global resultsFolder 
global userSettingsFile 
global defaultSettingsFile 

programFolder = Path("./ProgramFiles")
dataFolder = Path("../UserData")
resultsFolder = Path("../UserResults")
userSettingsFile = Path("../settings.ini")
defaultSettingsFile = Path("../default.ini")

# Helper Functions # 

# Check if a file exists and is valid 
def foundDataFile(input = ""): 
	path = dataFolder / input
	exists = path.exists()
	isFile = path.isfile()
	if exists and isFile:
		return True
	else:
		return False 

# Gets data from file
# Returns a list of lists
def getDataFromFile(filename):

	# Get file 
	try: 
		formattedData = []
		with open(filename) as f:
			objects = json.load(f)
	except: 
		print("Something went wrong. We can't access data from ", filename, "Check that you have written the correct "
			"file name in settings.ini, that your data is in UserData, and that it is formatted correctly. See "
			"README for instructions. ")
		sys.exit(1) 

	# Get objects from file 
	for o in objects: 
		try: 
			name = o.get("name")
			label = o.get("label")
			abrv = o.get("abbreviation")
			data = o.get("data")
		except: 
			print("Something went wrong. Check that your data file is formatted correctly.\n")
			sys.exit(1) 
		
		# Check data is nonempty
		try: 
			assert(data != None and data != [])
		except: 
			print("Error: No data provided for", name, "\n")
			sys.exit(1) 

		# Check all data is between 0 and 1 
		try: 
			for d in data: 
				assert(0 <= d <= 1)
		except:
			print("Error: All data points must be in range [0,1] inclusive. Error found in:", name, "\n") 
			sys.exit(1) 

		# Add data to result 
		formattedData.append([name, label, abrv, data])

	# Return result 
	return formattedData

# Process settings.ini file 
# Returns a dictionary of settings 
def getSettings(filepath):
	settings = {}
	try: 
		parser = configparser.ConfigParser()
		parser.read_file(open(filepath))
	except: 
		print("Something went wrong. Cannot open settings.ini.")

	for section in parser.sections():
		settings[section] = {}
		for option in parser.options(section):

			if option == 'verbose' or option == 'interactive':
				settings[section][option] = parser.getboolean(section, option)

			# Check that a data file is provided 
			try:
				if option == 'data_filename':
					file = parser.get('data_settings', 'data_filename')
					assert(file != "" and file != None)  
			except: 
				print("Error: You must provide a data file. See the README file for instructions.")
				sys.exit(1)

			# Check that options are the right kind and that we can acess them 
			try: 
				if option == 'verbose':
					v = parser.get('general_settings', 'verbose')
					assert(v == "True" or v == "False")
			except: 
				print("Error: Verbose option must be either True or False.")

			try:  
				settings[section][option] = parser.get(section, option)
			except: 
				print("Something went wrong. Ensure that all section and option names in settings.ini have not been modified.")
				sys.exit(1)
	return settings

# Sets all default settings
# Returns nothing - should modify default.ini if necessary 
def setAllDefaults(filepath, modelNumber = -1): 

	try: 
		# Get initial settings 
		settings = configparser.ConfigParser(allow_no_value = True)
		settings.read_file(open(filepath))

		try: 
			assert(modelNumber >= -1)
			modelName = MODEL_LIST[int(modelNumber)].__name__
		except: 
			modelName = "Model" + str(modelNumber)

		# Make default paths for result and graph files 
		resultFileName = ("Result_" + modelName + "_" + today.strftime("%d-%m-%Y"))
		graphFileName = ("Graph_" + modelName + "_" + today.strftime("%d-%m-%Y")) 

		# General Settings
		settings['general_settings']['interactive'] = "True"
		settings['general_settings']['verbose'] = "False"

		# Data Settings
		settings['data_settings']['model_number'] = "0" 
		settings['data_settings']['result_filename'] = str(resultFileName)

		# Graph Settings 
		settings['graph_settings']['graph_filename'] = str(graphFileName)
		settings['graph_settings']['graph_caption'] = ""
		settings['graph_settings']['graph_x_label'] = ""
		settings['graph_settings']['graph_y_label'] = ""
		settings['graph_settings']['graph_legend_label'] = "Legend"

		with open(filepath, 'w') as configfile:
			settings.write(configfile)
	except: 
		print("Something went wrong. Ensure that default.ini has not been modified.")
		sys.exit(1)

	return 0 

# Fills in blank values with the default value.
# Returns nothing - should modify settings.ini if necessary 
def fillInDefaults(filepath, defaultSettingsFile): 
	try: 
		# Get default settings
		default = configparser.ConfigParser()
		default.read_file(open(defaultSettingsFile))

		# Get initial settings 
		settings = configparser.ConfigParser()
		settings.read_file(open(filepath))

		# try: 
		for section in settings.sections():
			for option in settings.options(section):
				if settings[section][option] == "" or settings[section][option] is None: 
					d = default[section][option]
					settings.set(section, option, d)
		with filepath.open('w') as configfile:
			settings.write(configfile)
	except: 
		print("Something went wrong. Ensure that default.ini has not been modified and that the sections and option names in"
			"settings.ini have not been modified.")
		sys.exit(1)

	return 0 







