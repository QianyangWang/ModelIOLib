This is a part of the source codes of a BTOPMC calibration software developed by Qianyang Wang (Beijing Normal University).
The functionalities in these modules can be used to read and write the BTOPMC parameter files.

Use the form_param_sequence() (the path of parameter files should be given as arguments) function in ParamIO.py can generate a numpy array of parameters,
this array can be used in optimization algorithms. Use the write_params() in ParamIO.py to write the modified parameters into the corresponding parameter files.

The full version of the calibration software with a GUI would be relased in the future. 
