'''
commandline.py
Command line interface for model fitting.
'''

# Imports #

import sys
import os
import configparser
from pathlib import Path

from models import * 
from modelfitting import *
from fileParser import * 

# Main Interface #

# Main function. Runs CLI or gets input from settings.ini
def runAll(): 

	# Open user settings file 
	userSettings = configparser.ConfigParser()
	userSettings.read_file(open(userSettingsFile))

	# Get interactive if possible
	try: 
		interactive = userSettings.getboolean('general_settings','interactive')
	except: 
		print("Error: The interactive setting (in settings.ini) requires a boolean input. Write True or False.")

	# Get model if possible
	try: 
		model = userSettings.getint('data_settings','model_number')
	except: 
		model = -1

	# Open user settings file 
	userSettings = configparser.ConfigParser()
	userSettings.read_file(open(userSettingsFile))

	# Set and fill in default settings
	setAllDefaults(defaultSettingsFile, model) 
	fillInDefaults(userSettingsFile, defaultSettingsFile)
	
	# Run program (interactive or non-interactive)
	if interactive: 
		print("\nRunning in interactive mode. See README for instructions.\n")
		runCLI(userSettingsFile)
	else: 
		print("\nRunning in automatic mode. See README for more information.\n")
		runAutomatic(userSettingsFile)

# This runs modelFitting automatically based on the information provided in settings.ini 
# This is not interactive, so it is faster to run the program multiple times. 
def runAutomatic(settingsFile):

	# Get settings 
	settings = configparser.ConfigParser()
	settings.read_file(open(settingsFile))

	# Get data from data file
	dataFileName = settings["data_settings"]["data_filename"].strip('\"')
	dataFilePath = dataFolder / dataFileName
	userData = getDataFromFile(dataFilePath) 

	# Get output file 
	outputFileName = settings["data_settings"]["result_filename"].strip('\"')
	outputFilePath = resultsFolder / outputFileName

	# Set output to file 
	with outputFilePath.open("w") as outputFilePath:
		sys.stdout = outputFilePath
	
		# Call model fitting main function 
		runModelFitting(settings, userData)

		# Reset output to stdout 
		sys.stdout = sys.__stdout__

	print("\nModel Fitting Complete. See UserResults.")
	return 0 


# This is an interactive command line 
# It prompts the user for necessary information and stores it in settings.ini
def runCLI(settingsFile):

	# Get settings 
	settings = configparser.ConfigParser()
	settings.read_file(open(settingsFile))

	# Get settings for easy access 
	verbose = settings["general_settings"]["verbose"]
	
	# MODEL NUMBER # 
	print("The following models are supported:")
	for i, model in enumerate(MODEL_LIST): 
		print(i, model.__name__)

	# Bad input handling (check if number is not valid)
	modelNumber = input("\nPick a model to use: ")
	while processNumberChoice(modelNumber, MODEL_LIST) is None: 
		print("Unexpected input. Pick a number that is shown above. ")
		modelNumber = input("\nPick a model to use: ")
		if processNumberChoice(modelNumber, MODEL_LIST) is not None:
			break 

	# Show model choice and write to settings 
	model = MODEL_LIST[int(modelNumber)]
	settings['data_settings']['model_number'] = str(modelNumber)
	print("MODEL: ", model.__name__)
	
	# DATA FILE #  
	print("\nPlace data files inside the UserData folder. Below, specify which file you would like to use.")
	showFiles = input("Show files? ")
	if processTrueFalse(showFiles):
		files = os.listdir(dataFolder)
		print('\n'.join(files))
		print('\n')

	# Get filepath 
	dataFileName = input("Enter filename: ")
	dataFilePath = dataFolder / str(dataFileName)

	# Bad input handling (check if file exists)
	while not dataFilePath.exists() or dataFileName == "": 
		print("We couldn't find that file. Make sure that the file is placed in the UserData folder. ")
		dataFileName = input("Enter filename: ")
		dataFilePath = dataFolder / str(dataFileName)
		if dataFilePath.exists():
			break 

	# Get data from file and write filename to settings 
	settings['data_settings']['data_filename'] = str(dataFileName)
	userData = getDataFromFile(dataFilePath)


	# OUTPUT FILE #
	print("\nSpecify a result file name. If left blank, the default will be used. \nNote: If this file does not "
		"exist then it will be created. If this file already exists it will be overwritten.")
	outputFile = input("Enter filename: ")

	# Use default output file if necessary 
	if outputFile is None or outputFile == "": 
		outputFile = settings['data_settings']['result_filename']
	outputFilePath = resultsFolder / outputFile

	# Write new non-default to settings if necessary 
	settings['data_settings']['result_filename'] = str(outputFile)

	# GRAPH FILE # 
	print("\nSpecify a graph file name. If left blank, the default will be used. \nNote: If this file does not "
		"exist then it will be created. If this file already exists it will be overwritten.")
	graphFile = input("Enter filename: ")

	# Use default output file if necessary 
	if graphFile is None or graphFile == "": 
		graphFile = settings['graph_settings']['graph_filename']
	graphFilePath = resultsFolder / graphFile

	# Write new non-default to settings if necessary 
	settings['graph_settings']['graph_filename'] = str(graphFile)


	# GRAPH DETAILS # 
	setGraphOptions = input("\nWould you like to specify graph labels and captions? ")
	if processTrueFalse(setGraphOptions): 

		# GRAPH CAPTION #

		graphCaption = input("Write the caption for your graph.\n")
		settings['graph_settings']['graph_caption'] = str(graphCaption)

		# GRAPH X LABEL # 

		graphXLabel = input("Write the x axis label for your graph.\n")
		settings['graph_settings']['graph_x_label'] = str(graphXLabel)

		# GRAPH Y LABEL # 

		graphYLabel = input("Write the y axis label for your graph.\n")
		settings['graph_settings']['graph_y_label'] = str(graphYLabel)

		# GRAPH LEGEND LABEL # 

		graphLegendLabel = input("Write a legend label for your graph.\n")
		settings['graph_settings']['graph_legend_label'] = str(graphLegendLabel)

	# VERBOSE OPTION # 
	isVerbose = input("\nVerbose output? ")
	if processTrueFalse(isVerbose):
		verbose = True 

	# Write verbose to settings
	settings['general_settings']['verbose'] = str(verbose)

	# ROUNDING OPTION # 
	rounding = input("\nBy default results are rounded to five (5) significant digits. To change this, enter an integer: ")
	if processInteger(rounding) is not None:
		rounding = str(rounding)
		settings['general_settings']['rounding'] = str(rounding)

	# Save all settings changes
	with open(userSettingsFile, 'w') as configfile:
		settings.write(configfile)

	# Run Main ModelFitting #

	# Set output to file and run model fitting 
	with outputFilePath.open("w") as outputFilePath:
		sys.stdout = outputFilePath
	
		# Call model fitting main function 
		settingsDictionary = getSettings(userSettingsFile)
		try: 
			runModelFitting(settingsDictionary, userData)
		except: 
			print("Something went wrong. Ensure that settings.ini and models.py have been modified as needed. " 
				"Also check that the data file is located in UserData and contains well-formatted data. See README for instructions.")

		# Reset output to stdout 
		sys.stdout = sys.__stdout__

	print("\nModel Fitting Complete. See UserResults.")
	return 0 

# HELPER FUNCTIONS #

# True/False question helper function 
def processTrueFalse(input = ""):
	trueList = ["True", "true", "T", "t", "Y", "y", "yes", "Yes"]
	falseList = ["False", "false", "F", "f", "N", "n", "No", "no"]
	if input in trueList:
		return True
	if input in falseList: 
		return False 
	else: 
		return None

# Number choice question helper function 
def processNumberChoice(input = 0, choices = []): 
	try: 
		num = int(input)
		if 0 <= num < len(choices):
			return num 	
	except: 
		return None 

# Process number input 
def processInteger(input = ""): 
	try: 
		num = int(float(input))
		return num 
	except: 
		return None

# RUN MAIN #

runAll()

