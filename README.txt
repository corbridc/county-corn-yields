DVA_Project

https://github.gatech.edu/sschwarz8/DVA_Project

DESCRIPTION -
Yield prediction is an important part of any farming operation. It helps producers benchmark and understand their crop’s potential for the year. Lots of farmers have difficulty predicting yields and understanding what their upcoming corn will bring. The objective of this project is to provide a scenario planning tool to forecast corn crop yields on a county level. This tool will leverage state of the art models, XGBoost, leveraging highly researched covariates for prediction, such as days over 30 degrees Celsius. This tool allows users to adjust the covariates to develop scenarios and view the impacts to yield at a county level.
The dashboard is separated into two parts. The top portion of the page allows a user to enter their field location and other relevant parameters and get the modeled yield prediction for the field. This also shows the five year average yield in their county to allow the user to see how their predicted yield compares historical yield around them.  The bottom portion of the screen shows the user historical yield for a selected year and state that is broken out by county.


## Installation and Execution Steps
1. Clone this repo.
`$ git clone https://github.gatech.edu/sschwarz8/DVA_Project.git`
2. Enter repo directory.
`$ cd DVA_Project`
3. Create virtual environment.
`$ python -m venv dva_project_venv`
4. Activate virtual environment.
Windows:
`$ dva_project_venv\Scripts\activate`
Mac:
`$ source dva_project_venv/bin/activate`
5. Install dependencies.
`$ pip install -r requirements.txt`
6. Run the app.
`$ python app.py`
7. paste http://127.0.0.1:8050/ into your browser.

Demo Video: https://youtu.be/IEukuB70BEU
  minute 1: Getting Started with Corn Yield Prediction Tool 
  minute 2: Overview of tool features

*Please be aware that due to the classes project size limits the yield prediction feature will only work for the state of Iowa.

