How to run the models
=====================

A scenario folder contains three folders:

- InputData
- TEanalysis
- TEsimulation

The InputData folder contains various files with raw data. 
These data are cleaned and structured to be ready to be given 
as inputs to the model. The TEanalysis folder contains the Python 
functions that can be used for the post process of the results that 
are obtained as outputs from the model. The TEsimulation folder 
contains the main model.


TEsimulation folder
-------------------

This folder contains the following main items:

•	the AddFiles folder contains the inputs files to the model;
•	the Results folders contains the output results from the model in the form of files and figures;
•	runScenario.ipynb is the file that should be open with the Jupyter notebook interface. The overall model is launched by running this file;
•	the python files represent the different models that are part of the overall energy infrastructures (e.g. controllers, district heating supply plants and heat consumers)
•	the log files can be used for debugging the overall code when receiving an error from the overall simulation;
•	the remaining file (fmu and docker) are specific to the co-simulation approach of this model. Further information could be provided for advanced users of the model.

An advanced user, who wish to change the co-simulation structure (add/remove/modify models), should get a more in depth explanation of each of the above files. For the sake of running the models set up as it is, a user should focus on how to use the runScenario file.


How to use runScenario
^^^^^^^^^^^^^^^^^^^^^^

The script in this file is composed of the different steps that should be followed to set up a co-simulation:

•	define the meta-models;
•	defined the nodes, which are the instances of the models, based on common meta-models;
•	define the links among the nodes;
•	establish a simulation hierarchy within each co-simulation step;
•	set the length and the time step of the co-simulation;
•	run the co-simulation.

An advanced user, who wish to change the co-simulation structure (add/remove/modify models), should get a more in depth explanation of each of the above functions. For the sake of running the models set up as it is, a user should focus on the following functions:

•	set the name for the input supply and return temperature curves (the labels can be read here (*));
•	set a maximum value for the network mass flow rate in order to check the technical feasibility of the above inputs;
•	set the co-simulation length (from one hour up to 365 days).

After running the Jupyter Notebook scripts, a message will appear with a statement that refers to the simulation waiting for the local nodes. At this point, the user should run with a python command the file runLocals.py. Two subsequent questions will appear. The answer is 1 to both of them (the reference model for the buildings). This last step will launch for the co-simulation, which will take around one hour for a one year simulation.

A co-simulation run in Jupyter Notebook produces results that are:

•	displayed directly in the notebook;
•	saved as files;
•	saved as figures, when reproduced as plots.

The last two points of results are stored in the Results folder, in the TEsimulation folder. In this same folder, after each co-simulation, two debug files are updated: activity.log and nodes.log. These files can be read as text files to help debugging potential errors


Notes on the AddFiles folder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This folder contains the input data to the co-simulation set up. The following files can be either directly modified or can be replaced by working with the raw files in the folder InputData:

•	BBs_atemp contains the heated flow area of each building in the case study:
•	BlocksData is a sum up of different input files for each building in the case study. The heated floor area values are stored here as well;
•	DHlosses contains the hourly curve for the reference network heat losses;
•	DHsupplyAvailability contains the time availability profiles for the different plants included in the heat supply mix;
•	(*) TR and TS contains the hourly profiles for the return and supply temperatures.

The following files require further advanced explanation to be changed:

•	Dhw.txt is the profile for the domestic hot water utilisation in the buildings;
•	InternalGains1.txt is the profile for the internal heat gains in the buildings;
•	Weather_Stockholm2022 is the profile for the outdoor temperature.

These files are linked to the FMU (Functional Mock-up Interface) for the Modelica model of the buildings. If a change should be made, the FMU should be updated as well, which require a more advanced explanation.


TEanalysis folder
-----------------

This folder contains the following main items:

- a Results folder to store the results produced by the below files;
- a file responsible for processing the results stored in the Results folder located in TEsimulation;
- a file for running the technical analysis;
- a file for running the economic analysis; 
- a file for running the environmental analysis;
- a file for creating the plots for:

  - cumulative and hourly heat load curves
  - hourly mass flow rate
  - hourly outdoor temperature
  - hourly supply and return temperatures

A user who wish to run a complete analysis should launch with a python command:

•	run_Environmental.py (which activate the other levels of analysis as well)
•	runPlots.py

All the results are stored in the Results folder.
