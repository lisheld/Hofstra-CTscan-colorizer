# Hofstra-CTscan-colorizer
An application to colorize grayscale CT scan images. 

Users select a DICOM file (.dcm) to colorize and can enter "bounds" and colors.

The "bounds" are the values in HU (Hounsfield Units) that define the ranges for which each color is applied. For example, if the bounds are -700 and 300, a pixel that has a HU value of less than -700 is one color, a pixel that is between -700 and 300 is a different color, and a pixel that is greater than 300 is a third color. Thus, there must be one more color than the amount of bounds. Colors apply from least to greatest, so the first color is for the lowest range, and the last color is for the highest range.

There is also a shading algorithm applied to each image. If a pixel is above the midpoint of it's defined range, it is lightened, and if it is below, it is darkened. The farther away from the midpoint it is, the stronger the effect. For example, if two bounds are defined as 0 and 100, and the color within the bounds is red, pixels larger than 50 would be a lighter shade of red, and those smaller than 50 would be a darker shade.

If no bounds are specified, the program will automatically generate a certain number of bounds depending on how large the actual image is (excluding the dead space around it).

If no colors are specified, the program randomly generates them.

# Required Dependencies:

- Matplotlib

- Pydicom

- Numpy

- Streamlit (For web app version)

# Setup:

- Accessible via website at https://share.streamlit.io/liamsheldonn/hofstra-ctscan-colorizer/main/dcm_colorizer_webapp.py

For running via computer:

- Download DCM_colorizer_webapp.py (for web app) or DCM_colorizer_CLI.py (for command line interface)
	
- For DCM_colorizer_CLI.py, change directory within code to where DICOM files are located.
	
- Colors and bounds can also be set manualy within DCM_colorizer_CLI.py (although code will run without them)
	
- For DCM_colorizer_webapp.py, no further setup is required. Simply run "streamlit run /path/to/file/DCM_colorizer_webapp.py" and go to http://localhost:8501/ in a web browser

# Syntax (command line version only):
	
- Colors should be entered as an n by 3 numpy array (n rows, 3 columns). 
	
- Each row represents a color, and each column is the the red, green, or blue component of that color.
	
- Format for colors is ((Red1, Green1, Blue1), (Red2, Green2, Blue2), ... , (RedN, GreenN, BlueN))
	
- If there are N colors, there should be N-1 bounds entered.
	
- Bounds should be entered as a list seperated by commas.
	
- Format for bounds is (Bound1, Bound2, Bound3,..., BoundN)
	
	
	

