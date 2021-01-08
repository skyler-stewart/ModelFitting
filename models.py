'''
models.py 
''' 

# Import tools 
import pandas as pd

# Define models to test here.

def flmpModel(a_params, v_params):
	predicted_values = []
	for a in a_params:
		for v in v_params:
			value = (a*v) / ((a*v) + ((1-a) * (1-v)))
			predicted_values.append(value)	

	# Return params and predicted values
	return a_params, v_params, predicted_values

def scModel(a_params, v_params, bias): 
	predicted_values = []
	for a in a_params:
		for v in v_params:
			value = (a*bias) + (v*(1-bias))
			predicted_values.append(value)	

	# Return params and predicted values
	return a_params, v_params, bias, predicted_values


# The model we want to use. 
MODEL = scModel
