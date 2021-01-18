'''
modelfitting.py
'''

import pandas as pd 
from scipy.optimize import curve_fit, least_squares
import math

# Uses scipy's least squares optimization 
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html
def fitModel(params, actualvalues):
	getRApplied = lambda p: getResiduals(actualvalues, p)
	result = least_squares(getRApplied, params, jac='3-point', bounds=(0,1))
	print(result)
	return list(result.x)

# Outputs a list of predicted av values (using Bayes theorem)
def generatePrediction(a_params, v_params): 
	# Apply Bayes to all combinations of a and v params
	predicted_values = []
	for a in a_params:
		for v in v_params:
			value = (a*v) / ((a*v) + ((1-a) * (1-v)))
			predicted_values.append(value)	

	# Return predicted values
	return a_params + v_params + predicted_values

# Compute and print residuals (actual - predicted)
# actualdata: data we fit to (all 35)
# args: params (list of a and v)
def getResiduals(actualdata, args): 
	# Generate prediction 
	args = list(args)
	a_params = args[0:5]
	v_params = args[5:10]
	prediction = generatePrediction(a_params, v_params)

	# Get residuals
	residuals = []
	for i in range(len(actualdata)):
		r = actualdata[i] - prediction[i] 
		residuals.append(r)

	return residuals

# Gets and prints the RMSD given a list of residuals
def getRMSD(residuals):
	rmsd = math.sqrt(sum([x**2 for x in residuals])/len(residuals))
	print("RMSD ", rmsd)
	return rmsd

def drawTable(a, v, av):  
	cols = ["A1", "A2", "A3", "A4", "A5", "None"]
	rows = ["V1", "V2", "V3", "V4", "V5", "None"]

	a = [round(i, 3) for i in a]
	v = [round(j, 3) for j in v]
	av = [round(k, 3) for k in av]
	
	groups = [av[i:i+5] for i in range(0, 25, 5)]
	groups.append(a)
	for i in range(0, 5):
		groups[i].append(v[i])

	table = pd.DataFrame(groups, columns = cols, index = rows)
	print(table)


#####################################################################################################################################################################
# DATA 

# Hypothetical Data 
# a_original = [0.10, 0.30, 0.50, 0.70, 0.90] 
# v_original = [0.05, 0.2, 0.45, 0.75, 0.80] 
# av_original = [0.05, 0.15, 0.25, 0.75, 0.95, 0.15, 0.35, 0.50, 0.70, 0.85, 0.10, 0.30, 0.50, 0.70, 0.90, 0.20, 0.40, 0.60, 0.80, 0.90, 0.30, 0.45, 0.75, 0.85, 0.95]

# Real Data 
a_original = [0.01, 0.04, 0.23, 0.94, 0.99]
v_original = [0.03, 0.44, 0.82, 0.93, 0.97]
av_original = [0.02, 0.02, 0.07, 0.53, 0.76, 0.03, 0.09, 0.20, 0.81, 0.94, 0.13, 0.20, 0.46, 0.96, 0.99, 0.27, 0.41, 0.68, 0.96, 0.99, 0.28, 0.50, 0.70, 0.99, 0.99]

#####################################################################################################################################################################
# MAIN 

# Format original data for later use
original_params_list = a_original + v_original
original_table = a_original + v_original + av_original
original_prediction = generatePrediction(a_original, v_original)

# Fit model (get optimal a and v parameters) and generate prediction from them 
result = fitModel(original_params_list, original_table)
a_result = result[0:5]
v_result = result[5:10]
optimized_prediction = generatePrediction(a_result, v_result)

# Format optimal prediction for later use 
a_opt = optimized_prediction[0:5]
v_opt = optimized_prediction[5:10]
av_opt = optimized_prediction[10:]

# Print Tables
print()
print("Original Data")
drawTable(a_original, v_original, av_original)
print()
print("Initial Prediction")
drawTable(a_original, v_original, original_prediction[10:])
print()
print("Optimal Prediction")
drawTable(a_opt, v_opt, av_opt)

# Print Parameters
print()
print("Original A Values ", a_original)
print("Optimal A Values ", a_opt)
print()
print("Original V Values", v_original)
print("Optimal V Values", v_opt)

# Print RMSDs
print()
print("Original Prediction RMSD")
residuals = getResiduals(original_table, original_prediction)
getRMSD(residuals)
print()
print("Optimized Prediction RMSD")
residuals = getResiduals(original_table, optimized_prediction)
getRMSD(residuals)


