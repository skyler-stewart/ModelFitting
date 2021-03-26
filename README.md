# Model Fitting

Description and general information. 

Optimal values are obtained using scipy least squares optimization: 
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html 


## Installation 

TBD 

## Overview 

There are three folders in the application:

1. UserData
Where you will place data files. 
2. UserResults 
Where the results of the model fitting will appear. 
3. ProgramFiles
Contains the model fitting code. You don't need to modify anything inside this folder. 

## Creating a Model 

To create a model, you will need to modify the models.py file. A model could look like this: 

'''
1 def exampleModel(parameter1, parameter2): 
2 	prediction = []
3	for p1 in parameter1:
4		for p2 parameter2:
5			value = p1 * p2 
6			prediction.append(value)	
7	return parameter1, parameter2, prediction 
8	
9 MODEL_LIST = [exampleModel, anotherModel, ... ] 
'''

1. Define the name of our model and its input parameters. You can include as many input parameters as you want. 
2. Make an empty list that will store each prediction. 
3. Loop through each parameter. Parameters on the outside are the "slower moving" parameter, while the ones used in the inner loop are "faster moving". 
5. Calculate a prediction given a value for the first parameter and the second parameter. This can be any kind of equation you want.
6. Here we store the prediction we just calculated in the prediction list. 
7. Now that we have generated predictions for all points, we return them. 
9. Be sure to add the name of your model to 'MODEL_LIST'. 


## Data Input 

To input data, you will need to create or modify files in the UserData folder. Currently, data must be input in JSON format. It looks like this: 

'''
[
	{
		"name": "parameter1", 
		"data": []
	},
	{
		"name": "parameter2", 
		"data": []
	}, 
	{
		"name": "observed", 
		"data": []
	}
]
'''

The **name** fields should be the same as the input parameters passed to your model. The **observed** field should include the data you want the model to fit to. 

## Model Fitting

## Results 
