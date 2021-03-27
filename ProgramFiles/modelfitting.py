'''
modelfitting.py

Uses scipy's least squares optimization
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
''' 

# Imports # 

import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm 
from scipy.optimize import curve_fit, least_squares
from scipy import interpolate

import inspect
from pathlib import Path
from collections.abc import Iterable

from models import * 
from fileParser import * 

# Main interface 
def runModelFitting(settings, data):

	# Settings for easy access 
	modelNumber = int(settings["data_settings"]["model_number"])
	model = MODEL_LIST[modelNumber]
	modelSignature = [p.name for p in inspect.signature(model).parameters.values()]

	# Call fitModel
	result = fitModel(settings, data)

	# Get observed (original) data
	oParams = [[t[0], t[1], t[2], t[3]] for t in data if t[0] in modelSignature]
	observedParams = []
	for i in oParams:
		observedParams.append(i)
	observedComposite = [[t[0], t[1], t[2], t[3]] for t in data if t[0] == "composite"][0]

	# Get final predicted (optimized) data
	pParams = observedParams
	for i, p in enumerate(result): 
		pParams[i][-1] = p

	predictedParams = []
	for i in pParams:
		predictedParams.append(i)
	prediction = model(*result)[-1]
	predictedComposite = observedComposite[0:2] + [prediction]

	# Call graphing 
	drawGraph2Factor(settings, observedParams, observedComposite, predictedParams, predictedComposite)
	

# Model Fitting Functions #
 
def fitModel(settings, data):

	# Settings for easy access
	verbose = settings["general_settings"]["verbose"]
	rounding = int(settings["general_settings"]["rounding"])
	modelNumber = int(settings["data_settings"]["model_number"])
	model = MODEL_LIST[modelNumber]
	modelSignature = [p.name for p in inspect.signature(model).parameters.values()]

	# Get parameter names, labels, abreviations, and data. 
	# Easy access for table and graph drawing. Is modified later to reflect optimal parameters.
	parameterData = [[t[0], t[1], t[2], t[3]] for t in data if t[0] in modelSignature]
	compositeData = [t for t in data if t[0] == "composite"][0]

	# Gets values from data input
	observedParameterValues = [t[-1] for t in data if t[0] in modelSignature]
	observedCompositeValues = [t[-1] for t in data if t[0] == "composite"][0]
		
	# Format (flatten) parameter list. 
	# These are parameters (free variables) that we can tweak.
	flatParams, paramIndex = flattenParameters(*observedParameterValues)

	# Combine all observed data (parameter and composite) into a single list. 
	# This is the data we fit against. 
	allObserved = flatParams + observedCompositeValues

	# Get optimal parameters (this is the model fitting)
	# We tweak parameters to minimize the difference between observed parameters + observed composite 
	# and optimized parameters + model prediction 
	result = least_squares(getResiduals, flatParams, args = (paramIndex, allObserved, settings, data), bounds=(0,1))
	resultParams = list(result.x)

	# Print result 
	print()
	print("Model Fitting Result")
	print()

	# Print scipy result if verbose enabled
	if verbose == "True" or verbose == "true":
		print(result)
		print()

	# Make final table (with optimal parameters)
	optimalParams = unflattenParams(resultParams, paramIndex)
	optimalPrediction = model(*optimalParams)[-1]

	# Replace initial data with optimal parameters 
	for i, optimal in enumerate(optimalParams): 
		parameterData[i][-1] = optimal

	# Draw optimal table 
	drawTable2Factor(parameterData, optimalPrediction, rounding)
	print()

	# Print and return optimal parameters (rounded)
	print("Optimal Parameters")
	print()
	for p in parameterData:
		values = p[-1]
		if isinstance(values, list): 
			for i, v in enumerate(values): 
				values[i] = round(v, rounding)
		else: 
			values = round(values, rounding)
		print(p[1], values)

	return optimalParams


# Compute and print residuals (actual - predicted)
def getResiduals(flatParams, paramIndex, allObserved, settings, data):

	# Get settings and data for easy access
	rounding = int(settings["general_settings"]["rounding"])
	verbose = settings["general_settings"]["verbose"]
	modelNumber = int(settings["data_settings"]["model_number"])
	model = MODEL_LIST[modelNumber]
	modelSignature = [p.name for p in inspect.signature(model).parameters.values()]

	parameterData = [[t[0], t[1], t[2], t[3]] for t in data if t[0] in modelSignature]

	# Generate prediction
	formattedParams = unflattenParams(flatParams, paramIndex)
	modelResult = model(*formattedParams) 

	# Print table if in verbose mode
	if verbose == "True" or verbose == "true": 
		prediction = modelResult[-1]
		# Replace initial data with optimal parameters 
		for i, p in enumerate(formattedParams): 
			parameterData[i][-1] = p 
		# Draw table 
		drawTable2Factor(parameterData, prediction, rounding)

	# Format prediction
	formattedPrediction = []
	for m in modelResult:
		if hasattr(m, "__len__"):
			formattedPrediction.extend(m)
		else: 
			formattedPrediction.append(m)

	# Get residuals
	residuals = []
	for i in range(len(allObserved)):
		r = allObserved[i] - formattedPrediction[i] 
		residuals.append(r)

	rmsd = round(getRMSD(residuals), rounding)
	print("RMSD = ", rmsd)
	print()

	return residuals

# Gets the RMSD given a list of residuals
def getRMSD(residuals):
	rmsd = math.sqrt(sum([x**2 for x in residuals])/len(residuals))
	return rmsd


# Drawing Functions #

# Draws a display table for data (second parameter is fastest moving)
# Columns are parameter 1, rows are parameter 2
def drawTable2Factor(paramData, compositeData, rounding = 5):  

	# Round parameter data (we can put this in a separate function later)
	for p in paramData:
		if isinstance(p[-1], Iterable): 
			p[-1] = list(p[-1])
			for i, v in enumerate(p[-1]): 
				p[-1][i] = round(v, rounding)
		else: 
			p[-1] = round(p[-1], rounding)

	# Round composite data
	compositeData = [round(c, rounding) for c in compositeData]

	# Get parameter information for easy access (hardcoded for now)
	param1Label = paramData[0][1]
	param1Abrv = paramData[0][2]
	param1Data = paramData[0][3]

	param2Label = paramData[1][1]
	param2Abrv = paramData[1][2]
	param2Data = paramData[1][3]

	# Get size of table 
	param1Length = len(param1Data) 
	param2Length = len(param2Data) 
	compositeSize = param1Length * param2Length
	assert(compositeSize == len(compositeData))

	# Make rows (each group is a row) from composite data 
	groups = [compositeData[i:i+param1Length] for i in range(0, compositeSize, param1Length)]

	# Combine rows into table 
	groups.append(param1Data)
	for i in range(0, param1Length):
		groups[i].append(param2Data[i])

	# Make column and row labels
	colLabel = [param1Abrv + str(i) for i in range (1, len(param1Data) + 1)] + [""]
	rowLabel = [param2Abrv + str(i) for i in range (1, len(param2Data) + 1)] + [""]

	# Output table and other params 
	table = pd.DataFrame(groups, columns = colLabel, index = rowLabel)
	print(table)

	for p in paramData[2:-1]:
		values = p[-1]
		if isinstance(values, list): 
			for i, v in enumerate(values): 
				values[i] = round(v, rounding)
		else: 
			values = round(values, rounding)
		print(p[1], values)

# Draws graph 
# Observed values = points, predictions = lines
def drawGraph2Factor(settings, observedParams, observedComposite, predictedParams, predictedComposite):

	# Get settings 
	modelNumber = int(settings["data_settings"]["model_number"])
	model = MODEL_LIST[modelNumber]

	fileName = settings["graph_settings"]["graph_filename"]
	caption = settings["graph_settings"]["graph_caption"]
	xLabel = settings["graph_settings"]["graph_x_label"]
	yLabel = settings["graph_settings"]["graph_y_label"]
	legendLabel = settings["graph_settings"]["graph_legend_label"]

	# Get parameter labels
	P1Label = observedParams[0][1]
	P1Abrv = observedParams[0][2]

	P2Label = observedParams[1][1]
	P2Abrv = observedParams[1][2]

	# Get observed and predicted data 
	observedP1Data = observedParams[0][3]
	observedP2Data = observedParams[1][3]

	predictedP1Data = predictedParams[0][3]
	predictedP2Data = predictedParams[1][3]

	# Get parameter and composite size 
	param1Length = len(observedP1Data) 
	param2Length = len(observedP2Data) 
	compositeSize = param1Length * param2Length

	# Graph label processing
	if legendLabel == "" or legendLabel is None:
		legendLabel = P2Label

	# Set up Graph 
	plt.figure(figsize=(12, 8))
	plt.title(model.__name__)
	plt.xlabel(xLabel)
	plt.ylabel(yLabel)
	plt.figtext(0.5, 0.01, caption + "\n", wrap=True, horizontalalignment='center', fontsize=10)

	# Set line and point color scheme 
	color_interval = np.linspace(0, 1, param1Length+1)
	colors = [cm.plasma(x) for x in color_interval]

	# Group data
	# Note: this assumes that the first parameter is the "fastest moving" and that we will be graphing the first two parameters 
	groups_observed = [observedComposite[-1][i:i+param1Length] for i in range(0, compositeSize, param1Length)]
	groups_prediction = [predictedComposite[-1][i:i+param1Length] for i in range(0, compositeSize, param1Length)]

	# Define x axis range (discrete)
	xRange = [i for i in range(1, param1Length + 1)]

	# Plot observed values (dots)
	plt.scatter(xRange, observedP1Data, label = ('None'), marker = '.', s = 50, color = colors[0])
	for i in range(len(observedP1Data)): 
		plt.scatter(xRange, groups_observed[i],  label = (P2Abrv + str(i+1) +  ' = ' + str(round(observedP2Data[i],3))), marker = '.', s = 50, color = colors[i+1]) 

	# Plot model prediction after optimization (lines)
	plt.plot(xRange, predictedP1Data, color = colors[0])
	for i in range(len(predictedP1Data)):
		plt.plot(xRange, groups_prediction[i], color = colors[i + 1])

	# Plot legend
	plt.legend(loc="upper left", title=legendLabel, markerscale=1.5)

	# Export image
	if fileName is None or fileName == "": 
		plt.savefig('graphResult.png')
	else:
		filePath = resultsFolder / fileName
		plt.savefig(filePath)

# Helper Functions # 

# Returns the start and end index of each parameter
def indexParams(*params):
	# Determine size of each parameter group (how many of each kind)
	countList = [0]
	for p in params:
		if isinstance(p, list):  
			countList.append(len(p))
		else: countList.append(1)

	# Get number of parameter groups
	numGroups = len(countList)

	# Get starting and ending index of each parameter group
	paramIndex = []
	currentIndex = 0 
	for i in range(numGroups):
		paramIndex.append(currentIndex + countList[i])
		currentIndex += countList[i]
	return paramIndex


# Transforms a flat list of params into multi-dimensional list of prediction params
# flattenedParams: parameters formatted as a one-dimensional list of values
# paramIndex: starting and ending indexes for each parameter group (use output of indexParams)
def unflattenParams(flattenedParams, paramIndex):
	# Get number of parameter groups
	numGroups = len(paramIndex) - 1
	unflat = []
	currentGroup = 0 

	# Fills paramList with correct values 
	for i in range(len(paramIndex) - 1): 
		start = paramIndex[i]
		end = paramIndex[i+1]
		paramGroup = flattenedParams[start:end]
		if len(paramGroup) > 1: 
			unflat.append(flattenedParams[start:end])
		else: 
			unflat.append(flattenedParams[start])
		currentGroup += 1

	return unflat


# Produces a one-dimensional list of free variables given any number of parameters in list format
def flattenParameters(*params): 
	flattened = []
	for i in params: 
		if isinstance(i, list):
			for j in i: 
				flattened.append(j)
		else: 
			flattened.append(i) 
	index = indexParams(*params)
	return flattened, index 


# DATA (FOR MANUAL TESTING) #

# Data 1 (Hypothetical Data) 
# a_original = [0.10, 0.30, 0.50, 0.70, 0.90] 
# v_original = [0.05, 0.2, 0.45, 0.75, 0.80] 
# av_original = [0.05, 0.15, 0.25, 0.75, 0.95, 0.15, 0.35, 0.50, 0.70, 0.85, 0.10, 0.30, 0.50, 0.70, 0.90, 0.20, 0.40, 0.60, 0.80, 0.90, 0.30, 0.45, 0.75, 0.85, 0.95]
# bias = 0.5

# Data 2 (Real Data) 
# a_original = [0.01, 0.04, 0.23, 0.94, 0.99]
# v_original = [0.03, 0.44, 0.82, 0.93, 0.97]
# av_original = [0.02, 0.02, 0.07, 0.53, 0.76, 0.03, 0.09, 0.20, 0.81, 0.94, 0.13, 0.20, 0.46, 0.96, 0.99, 0.27, 0.41, 0.68, 0.96, 0.99, 0.28, 0.50, 0.70, 0.99, 0.99]
# bias = 0.5

# Data 3 (Debugging Data)
# a_original = [0.05, 0.18, 0.45, 0.71, 0.89]
# v_original = [0.10, 0.25, 0.55, 0.82, 0.96]
# bias = 0.5

# Data 4 (6x6 data)
# a_original = [0, 0.01, 0.04, 0.23, 0.94, 0.99]
# v_original = [0, 0.03, 0.44, 0.82, 0.93, 0.97]
# av_original = [0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.001, 0.007, 0.028, 0.03, 0.0, 0.004, 0.018, 0.101, 0.414, 0.436, 0.0, 0.008, 0.033, 0.189, 0.771, 0.812, 0.0, 0.009, 0.037, 0.214, 0.874, 0.921, 0.0, 0.01, 0.039, 0.223, 0.912, 0.96]
# bias = 0.5

# MANUAL TESTING (Data 3) #

# Generate Predictions
# av_prediction_flmp = flmpModel(a_original, v_original)
# av_prediction_sc = scModel(a_original, v_original, bias)

# rounded1 = [round(r, 3) for r in av_prediction_flmp[-1]]
# print("FLMP Prediction ", rounded1)
# drawTable(a_original, v_original, av_prediction_flmp[-1])
# print()
# rounded2 = [round(r, 3) for r in av_prediction_sc[-1]]
# print("SC Prediction ", rounded2)
# print("Bias ", av_prediction_sc[-2] )
# drawTable(a_original, v_original, av_prediction_sc[-1])
# print()

# Test 1 - FLMP Prediction, FLMP Fit (RMSD should be 0)
# print("TEST 1")
# result1 = fitModel(av_prediction_flmp[-1], a_original, v_original)
# roundedresult1 = [round(r, 3) for r in result1]
# print(roundedresult1)

# Test 2 - FLMP Prediction, SC Fit (RMSD should be relatively high)
# print("TEST 2")
# result1 = fitModel(av_prediction_flmp[-1], a_original, v_original, bias)
# roundedresult1 = [round(r, 3) for r in result1]
# print(roundedresult1)

# Test 3 - SC Prediction, SC Fit (RMSD should be 0)
# print("TEST 3")
# result1 = fitModel(av_prediction_sc[-1], a_original, v_original, bias)
# roundedresult1 = [round(r, 3) for r in result1]
# print(roundedresult1)

# Test 4 - SC Prediction, FLMP Fit (RMSD should be relatively low)
# print("TEST 4")
# result1 = fitModel(av_prediction_sc[-1], a_original, v_original)
# roundedresult1 = [round(r, 3) for r in result1]
# print(roundedresult1)


# MAIN (FOR MANUAL TESTING) #

# Run model fitting
# result = fitModel(av_original, a_original, v_original)
# roundedresult = [round(r, 3) for r in result]
# print(roundedresult)

# # Draw Graph
# prediction = flmpModel(result[0:5], result[5:10])
# drawGraph(a_original, v_original, av_original, result[0:5], result[5:10], prediction[-1])

# mult = []
# for v in v_original: 
# 	for a in a_original: 
# 		m = round(a*v, 3)
# 		mult.append(m)
# print(mult)


# cols = ["Aparam1", "Aparam2", "Aparam3", "Aparam4", "Aparam5", "Aparam6", "None"]
# rows = ["Vparam1", "Vparam2", "Vparam3", "Vparam4", "Vparam5", "Vparam6", "None"]


# print("\nDRAWTABLE2FACTOR")
# drawTable2Factor(av_original, a_original, v_original, cols, rows)

