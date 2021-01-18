'''
modelfitting.py

Uses scipy's least squares optimization
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
''' 

# Import tools 
from scipy.optimize import curve_fit, least_squares
from models import * 
import numpy as np
import math
import matplotlib.pyplot as plt


# base: data points (not parameters). Part of the data we fit to. 
# params: parameters from which we will generate a prediction 
def fitModel(base, *params):

	# Format parameter list
	paramIndex = indexParams(*params)
	flatParams = flattenParameters(*params) 
	newBase = flatParams + base
	initialPrediction = flatParams 

	# Intermediate step: generate a prediction and get residuals (reformatted)
	#getRApplied = lambda p: getResiduals(p, paramIndex, newBase)
	#result = least_squares(getRApplied, flatParams, jac='3-point', bounds=(0,1)) 

	# Get optimal parameters 
	result = least_squares(getResiduals, initialPrediction, args = (paramIndex, newBase), bounds=(0,1))

	print()
	print(result)
	print()
	print("Model = ", MODEL.__name__)
	print("Optimal Parameters")
	return list(result.x)


# Compute and print residuals (actual - predicted)
# base: data points (not parameters). Data we fit to. 
# flattenedParams: parameters formatted as a one-dimensional list of values
# paramIndex: start and end index of each group of parameters (use output of indexParams)
def getResiduals(flattenedParams, paramIndex, base):

	# Generate prediction
	formattedParams = unflattenParams(flattenedParams, paramIndex)
	modelResult = MODEL(*formattedParams) 

	# Note: drawTable has not been generalized yet, so this will change
	drawTable(formattedParams[0], formattedParams[1], modelResult[-1])

	# Format prediction
	formattedPrediction = []
	for m in modelResult:
		if hasattr(m, "__len__"):
			formattedPrediction.extend(m)
		else: 
			formattedPrediction.append(m)

	# Get residuals
	residuals = []
	for i in range(len(base)):
		r = base[i] - formattedPrediction[i] 
		residuals.append(r)

	print("Bias = ", modelResult[2])
	print("RMSD = ", getRMSD(residuals))
	print()

	return residuals



# Gets the RMSD given a list of residuals
def getRMSD(residuals):
	rmsd = math.sqrt(sum([x**2 for x in residuals])/len(residuals))
	return rmsd


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


# Produces a one-dimensional list of free variables given any number of parameters
def flattenParameters(*params): 
	flattened = []
	for i in params: 
		if isinstance(i, list):
			for j in i: 
				flattened.append(j)
		else: 
			flattened.append(i) 
				
	return flattened


# Displays a table of data
# This is not generalized yet 
def drawTable(a, v, av):  
	cols = ["A1", "A2", "A3", "A4", "A5", "None"]
	rows = ["V1", "V2", "V3", "V4", "V5", "None"]

	a = [round(i, 4) for i in a]
	v = [round(j, 4) for j in v]
	av = [round(k, 4) for k in av]

	groups = [av[i:i+5] for i in range(0, 25, 5)]
	groups.append(a)
	for i in range(0, 5):
		groups[i].append(v[i])

	table = pd.DataFrame(groups, columns = cols, index = rows)
	print(table)


# Draws graph
# This is not generalized yet)
def drawGraph(a_real, v_real, av_real, a_predicted, v_predicted, av_predicted):
#a_predicted=0, v_predicted, av_predicted, 
	# Setup Graph 
	plt.figure(figsize=(12, 8))
	plt.title(MODEL.__name__)
	plt.xlabel('Auditory Parameter Value')
	plt.ylabel('P(DA) Identification')
	#plt.style.use('dark_background')

	# Plot real data
	plt.scatter(a_real, a_real, label = ('None'), marker = '.', s = 50, color = 'gray')
	plt.scatter(a_real, av_real[0:5],   label = ('V1 = ' + str(v_real[0])), marker = '.', s = 50, color = 'mediumblue') 
	plt.scatter(a_real, av_real[5:10],  label = ('V2 = ' + str(v_real[1])), marker = '.', s = 50, color = 'purple') 
	plt.scatter(a_real, av_real[10:15], label = ('V3 = ' + str(v_real[2])), marker = '.', s = 50, color = 'crimson')  
	plt.scatter(a_real, av_real[15:20], label = ('V4 = ' + str(v_real[3])), marker = '.', s = 50, color = 'darkorange') 
	plt.scatter(a_real, av_real[20:25], label = ('V5 = ' + str(v_real[4])), marker = '.', s = 50, color = 'gold') 
	

	# Plot optimized model prediction
	plt.plot(a_predicted, a_predicted, color = 'gray')
	plt.plot(a_predicted, av_predicted[0:5], color = 'mediumblue')
	plt.plot(a_predicted, av_predicted[5:10], color = 'purple')
	plt.plot(a_predicted, av_predicted[10:15], color = 'crimson')
	plt.plot(a_predicted, av_predicted[15:20], color = 'darkorange')
	plt.plot(a_predicted, av_predicted[20:25], color = 'gold')
	

	# Plot legend 
	plt.legend(loc="upper left", title="Visual Parameter")

	# Export image
	plt.savefig('modelfitFLMP.png')


############################################################################

# DATA 
# Note: This will later be input from a file 

# Data 1 (Hypothetical Data) 
# a_original = [0.10, 0.30, 0.50, 0.70, 0.90] 
# v_original = [0.05, 0.2, 0.45, 0.75, 0.80] 
# av_original = [0.05, 0.15, 0.25, 0.75, 0.95, 0.15, 0.35, 0.50, 0.70, 0.85, 0.10, 0.30, 0.50, 0.70, 0.90, 0.20, 0.40, 0.60, 0.80, 0.90, 0.30, 0.45, 0.75, 0.85, 0.95]
# bias = 0.5

# Data 2 (Real Data) 
a_original = [0.01, 0.04, 0.23, 0.94, 0.99]
v_original = [0.03, 0.44, 0.82, 0.93, 0.97]
av_original = [0.02, 0.02, 0.07, 0.53, 0.76, 0.03, 0.09, 0.20, 0.81, 0.94, 0.13, 0.20, 0.46, 0.96, 0.99, 0.27, 0.41, 0.68, 0.96, 0.99, 0.28, 0.50, 0.70, 0.99, 0.99]
bias = 0.5

# Data 3 (Debugging Data)
# a_original = [0.05, 0.18, 0.45, 0.71, 0.89]
# v_original = [0.10, 0.25, 0.55, 0.82, 0.96]

#av_original = [0]*25

############################################################################

# MAIN 
# Note: This will be replaced with a CLI

# Run model fitting
result = fitModel(av_original, a_original, v_original)
roundedresult = [round(r, 3) for r in result]
print(roundedresult)

# Draw Graph
prediction = flmpModel(result[0:5], result[5:10])
drawGraph(a_original, v_original, av_original, result[0:5], result[5:10], prediction[-1])

