# FLMP Model Fitting
# To Do (and other ideas)
	# Dockerize (run reliably in any environment)
	# Add command line support and/or GUI 
	# Add support for data entry in multiple formats (JSON, CSV, etc.)

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Outputs a list of predicted av values (using Bayes theorem)
def preprocessing(a_params, v_params, a_weight = 1, v_weight = 1): 

	weighted_a_params = []
	weighted_v_params = []
	predicted_values = []

	# Weight a and v params if needed 
	for a in a_params:
		weighted_a_params.append(a * a_weight) 
	for v in v_params:
		weighted_v_params.append(v * v_weight)

	# Apply Bayes to all combinations of a and v params
	for a in weighted_a_params:
		for v in weighted_v_params:
			value = (a*v) / ((a*v) + ((1-a) * (1-v)))
			predicted_values.append(value)

	# Return predicted av values
	return predicted_values


# Defines the models we want to test (polynomial and hyperbolic tan as placeholders)
def cubicModel(x, a, b, c, d):
	x = np.asarray(x)
	return a*(x**3) + b*(x**2) + c*x + d

def tanhModel(x, a, b, c):
	x = np.asarray(x)
	return a*np.tanh(b*x) + c


# Fits the model function to the data
def fitModel(predicted_values, actual_values): 

	# Pick which model we want to use
	model = cubicModel

	# Set up graph 
	plt.figure(figsize=(12, 8))
	plt.title(model.__name__)
	plt.xlabel('Predicted Values')
	plt.ylabel('Actual Values')

	# Plot points (map predicted values to actual values)
	plt.scatter(predicted_values, actual_values, label = 'Data', marker = '.', s = 50, color = 'black') 

	# Fit the model (scipy's curve_fit should do the same thing as the Julia library) 
	# https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.curve_fit.html
	p, pc = curve_fit(model, predicted_values, actual_values, maxfev=10000)

	# Draw model 
	x_scale = np.linspace(0,1,num=10000)
	plt.plot(x_scale, model(x_scale, *p), label='Fitted function', color = 'gray')
	
	# Export image
	plt.savefig('modelfit.png')

	# Get RMSD 
	rmsd = np.mean((actual_values - model(predicted_values, *p)) ** 2)

	print("Model: ", model.__name__)
	print("Optimal Model Parameters: ", p)
	print("RMSD: ", rmsd)

#####################################################################################################################################################################

# Hypothetical Data 
# a_params = [0.10, 0.30, 0.50, 0.70, 0.90] 
# v_params = [0.05, 0.2, 0.45, 0.75, 0.80] 
# av_values = [0.05, 0.15, 0.25, 0.75, 0.95, 0.15, 0.35, 0.50, 0.70, 0.85, 0.10, 0.30, 0.50, 0.70, 0.90, 0.20, 0.40, 0.60, 0.80, 0.90, 0.30, 0.45, 0.75, 0.85, 0.95]

# Real Data 
a_params = [0.01, 0.04, 0.23, 0.94, 0.99]
v_params = [0.03, 0.44, 0.82, 0.93, 0.97]
av_values = [0.02, 0.02, 0.07, 0.53, 0.76, 0.03, 0.09, 0.20, 0.81, 0.94, 0.13, 0.20, 0.46, 0.96, 0.99, 0.27, 0.41, 0.68, 0.96, 0.99, 0.28, 0.50, 0.70, 0.99, 0.99]

predicted_values = preprocessing(a_params, v_params)
fitModel(predicted_values, av_values)






