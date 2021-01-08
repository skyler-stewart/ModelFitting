''' 
This file includes various functions that are not in use now, but may be helpful in the future. 
'''

def generatePrediction(a_params, v_params, a_weight = 1, v_weight = 1): 

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
			predicted_values.append(round(value, 3))

	# Return predicted values
	return a_params, v_params, predicted_values


# Definitions of models we want to test (polynomial and hyperbolic tan as examples)
def cubicModel(x, a, b, c, d):
	x = np.asarray(x)
	return a*(x**3) + b*(x**2) + c*x + d

def tanhModel(x, a, b, c):
	x = np.asarray(x)
	return a*np.tanh(b*x) + c


# Fits the model function 
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


# Fits the model function to grouped data (in progress)
def fitModelGrouped(predicted_values, actual_values): 

	# Pick which model we want to use
	model = tanhModel

	# Set up graph 
	plt.figure(figsize=(12, 8))
	plt.title('Grouped ' + model.__name__)
	plt.xlabel('Predicted Values')
	plt.ylabel('Actual Values')
	plt.ylim((0, 1))

	# Plot points (map predicted values to actual values)
	colors = ['red', 'green', 'blue', 'darkred', 'orange']
	for i in range(0, 25, 5): 
		index = int(i/5)
		plt.scatter(predicted_values[i:i+5], actual_values[i:i+5], marker = '.', s = 50, color = colors[index])

	# Fit the model (grouped by visual input)
	for i in range(0, 25, 5):
		p, pc = curve_fit(model, predicted_values[i:i+5], actual_values[i:i+5], maxfev=10000)

		# Plot model
		x_scale = np.linspace(0,1,num=10000)
		index = int(i/5)
		plt.plot(x_scale, model(x_scale, *p), color = colors[index])
	

	# Export image
	plt.savefig('modelfitgrouped.png')

	Get RMSD 
	rmsd = np.mean((actual_values - model(predicted_values, *p)) ** 2)

	print("Model: ", model.__name__)
	print("Optimal Model Parameters: ", p)
	print("RMSD: ", rmsd)

