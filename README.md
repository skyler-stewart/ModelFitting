# Model Fitting 

This is a command line application for model fitting. We currently support full factorial designs of two factors. Factors may have any number of discrete levels. 

Parameter optimization uses scipy least squares optimization: 
https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html 


## Installation (MacOS and Linux)

1. Clone (download) this GitHub repository. Use the green download button at the top of this page. 

2. You will also need Python3 installed to run this application. You can find it here: https://www.python.org/downloads/. Download and open the Python3 installer.

3. Using the Terminal application on your computer, navigate to the main ModelFitting directory. To do this, you will use a command similar to the following. This may be different depending on your operating system and download location. 
```
cd /Users/Username/Downloads/ModelFitting
```

4. Install all necessary dependencies. Run the following command: 
```
pip3 install -r requirements.txt 
```

Installation is now complete. Follow the instructions below to create and fit models. 


## Installation (Windows)

1. Clone (download) this GitHub repository. Use the green download button at the top of this page.

2. You will also need Python3 installed to run this program. We recommend using a miniConda environment. You can find the minConda installers here: https://docs.conda.io/en/latest/miniconda.html 

3. Create and enter a miniConda environment using the Anaconda Prompt application. Run the following commands in Anaconda Prompt: 
```
conda create --name myenv
activate myenv
```

4. Install pip3 and download dependencies using the following commands: 
```
conda install pip3
pip3 install -r requirements.txt 
```

Installation is now complete. Follow the instructions below to create and fit models. 

## Overview 

The following are important files and directories contained in the application. You will need to modify some of these files before running the program.  

**settings.ini**  
Where you define the program settings. You will need to modify this file. 

**models.py**  
Where you define models. You will need to modify this file. It is located inside the ProgramFiles directory.  

**UserData**   
Where you place data files. You will need to modify this folder's contents. 

**UserResults**   
Where the results will appear. Results include a text summary and a graph.

**ProgramFiles**  
Contains the application code. The models.py file is located in this directory. Do not modify other files in this folder. 

## Creating a Model 

To create a model, you will need to modify the models.py file. Here is an example of a model. We provide comments corresponding the the line number below.  

```python
# Note: The following is not a real model. It is simply provided as an example. 
1 def exampleModel(parameter1, parameter2): 
2    prediction = []
3	for p1 in parameter1:
4		for p2 in parameter2:
5			value = p1 * p2 
6			prediction.append(value)	
7	return parameter1, parameter2, prediction 
8	
9 MODEL_LIST = [exampleModel, anotherModel, ... ] 
```

(1) Define the name of our model and its input parameters. You can include as many input parameters as you want (note that only the first two parameters will be displayed in tables and graphed).  
(2) Make an empty list that will store each prediction.   
(3) Loop through each parameter. Parameters on the outside are "slower moving", while parameters in the inner loop are "faster moving".   
(5) Calculate a prediction given a value for the first parameter and for the second parameter. This can be any kind of equation you want.  
(6) Here we store the prediction we just calculated in the prediction list.  
(7) Now that we have generated predictions for all points, we can return the result. The output should include the values of each parameter followed by the prediction.     
(9) Be sure to add the name of your model to 'MODEL_LIST'. 


## Data Input 

To input data, you will need to create or modify files in the UserData folder. It is recommended that you copy and modify the provided template file, **template.json** that is in the UserData folder. Data must be in JSON format, and must fall in range [0,1] inclusive. Here is an example data file. 

```json
[
{
"name": "composite", 
"label": "composite", 
"abbreviation": "c", 
"data": [0.4, 0.5, 0.6, 0.8, 0.10, 0.12, 0.12, 0.15, 0.18]
},
{
"name": "parameter1", 
"label": "Parameter 1", 
"abbreviation": "P1", 
"data": [0.1, 0.2, 0.3]
},
{
"name": "parameter2",
"label": "Parameter 2", 
"abbreviation": "P2",  
"data": [0.4, 0.5, 0.6]
},
{
"name": "parameter3", 
"label": "Parameter 3", 
"abbreviation": "P3", 
"data": [0.7, 0.8, 0.9]
}
]
```

You should include a section for **each parameter** in your model, as well as a **composite** section. If you do not include these sections, errors may occur. You may include additional sections if you wish; only parameters included current model will be used. 

* The **parameter** fields are the observed values for each parameter. 
* The **composite** field are the observed values for every combination of pararmeters. 

Within these sections, you should include the following: 

* The **name** fields are the section names. 
    * For parameter sections, this should be the same as the input parameter passed to your model. Note that this is case-sensitive, so "Parameter1" is not the same as "parameter1". 
    * For the composite section, the name should be "composite". If it is named something else, this section will not be recognized correctly, and errors may occur. 
* The **label** fields are nicely formatted versions of the name. These will be used in the result file and graph when displaying data. 
* The **abbreviation** fields are shortened versions of the label or name. They are also used to display data. 
* The **data** fields should include a list of observed values. All values should be in range [0, 1] inclusive. 
    * Your model prediction will be fit against all values (the parameters and composite combined). 
    
## Settings

Now that you have created a model and a data file, you can modify the program settings. These are located in a file called **settings.ini**. You will see the following settings: 

**interactive**  
This determines whether the program will run in interactive mode. If this is set to **True**, then you will see a number of prompts on the command line which allow you to pick a model to test, the data file to use, and other options. You do not need to modify any other settings if you are using interactive mode. This is recommended if it is your first time using this program. If this option is set to **False** the program will run in automatic mode. The program will use the settings (from settings.ini) to run the program. If you leave any settings blank the default option will be used (except for **data_file**, which must be included). 

**verbose**   
This describes the level of detail that is written to the results file. If set to **True** this will display the parameters and model prediction at each step of the model fitting. Set this to **True** or **False**. 

**rounding**  
This describes the number of significant digits displayed in the result. This does not affect the results of the model fitting itself. By default, numbers will be rounded to five digits. Set this to an integer. 

**data_filename**   
This is the data file you would like to use. You must provide a file name that corresponds to a file in the UserData folder. 

**result_filename**   
Results will be written to this file (which will be placed in the UserResults folder) Note that if the file you provide already exists, it will be overwritten. 

**model_number**  
This is the model you would like to fit. Enter an integer that corresponds to the model's index in MODEL_LIST. Note that MODEL_LIST is zero indexed. 

**graph_filename**  
This is the graph result file. It will be placed in the UserResults folder. 

**graph_caption**  
This caption will displayed underneath your graph. Enter a string.  

**graph_x_label**  
This will create a label for the x-axis of your graph. Enter a string. 

**graph_y_label**  
This will create a label for the y-axis of your graph. Enter a string. 

**graph_legend_label**  
This will create a label for the graph legend. Enter a string. 

Here is an example configuration: 
```ini
[general_settings]
interactive = False
verbose = False
rounding = 3

[data_settings]
data_filename = exampledata.json
result_filename = Result_exampleData_exampleModel
model_number = 0

[graph_settings]
graph_filename = Graph_exampleData_exampleModel
graph_caption = This is a graph caption. 
graph_x_label = This is an x-axis label. 
graph_y_label = This is a y-axis label. 
graph_legend_label = Legend Label

```

Do not modify section titles or option names. Only modify text directly after the "=" sign.

## Model Fitting

Now we can fit our models. To run the program, navigate to the main directory (called ModelFitting). Then run the following command. 

```
$ ./runmodelfitting.sh
```
If this doesn't work, you may need to do the following first: 
```
$ chmod +x runmodelfitting.sh
```

Alternatively, you may simply navigate into the ProgramFiles directory and run the program directly:
```
$ cd ProgramFiles
$ python3 commandline.py
```

## Results 

Your results (a result file and a graph file) will appear in the UserResults folder. 

