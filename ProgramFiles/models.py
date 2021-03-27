'''
models.py 
''' 

# Import tools 
import pandas as pd
import numpy as np

# Define models to test here.

def exampleModel(parameter1, parameter2): 
    prediction = []
    for p1 in parameter1:
        for p2 in parameter2:
            value = p1 * p2 
            prediction.append(value)    
    return parameter1, parameter2, prediction 

def flmpModel(a_params, v_params):
	predicted_values = []
	for v in v_params:
		for a in a_params:
			value = (a*v) / ((a*v) + ((1-a) * (1-v)))
			predicted_values.append(value)	
	return a_params, v_params, predicted_values


def scModel(a_params, v_params, bias): 
	predicted_values = []
	for v in v_params:
		for a in a_params:
			value = (a*bias) + (v*(1-bias))
			predicted_values.append(value)	
	return a_params, v_params, bias, predicted_values


# A list of all models  
MODEL_LIST = [exampleModel, flmpModel, scModel] 

'''
NOTES 
The first parameter should be "fastest moving". In general, parameters should go in this order in 
relation to the composite data. See README for more information. 
'''
