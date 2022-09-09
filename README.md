Assignment 5 – Implementation of Serverless BERT
==============================

https://share.streamlit.io/sairaghav1999/streamlit/main/app.py

Introduction
==============================
As part of the fifth assignment of DAMG 7245 we had to design and build 2 more API's to call the NLP models which are created on serverless lambda fucntions **Summarization and Named Entity Recognition**. The user can enter any latitude and longitude value as input and the API will search for the nearest event to that latitude and longitude and return the forecast along with a summary and Named entity recognition of the event narrative.

The API endpoints are secured with JWT tokens and can be accessed only by authenticated users which are tracked in a BigQuery table and all the users have their associated tokens which are used to access the API endpoint to enable nowcasting.

Additionally, we have updated the web application so an authenticated user can only use upto 10 requests to call the API per day, All the calls are logged into the system and can be observed via a live dashboard.

The Dashboard reveals the user analytics and gives updated information on every user for the number of API calls and how many queries were invoked.

The Serverless lambda functions on AWS hosts the dockerized Summarization and NER models.

Architecture Diagram
==============================
![WhatsApp Image 2022-04-14 at 7 59 58 PM](https://user-images.githubusercontent.com/91291183/163495780-84abf74c-9faf-44af-8297-3a4ac480646a.jpeg)



Nowcasting system
==============================
* [Nowcasts](https://en.wikipedia.org/wiki/Nowcasting_(meteorology)) are short-term forecast of weather variables typically measured by weather radar or satellite.   Nowcasts are different from traditional weather forecasts in that they are based (mostly) on statistical extrapolations of recent data, rather than full physics-based numerical weather prediction (NWP) models.  
* Nowcast are computed in a variety of ways, but one of the most common approaches is to apply optical flow techniques to a sequence of radar images.   These techniques track the motion of storm objects, which is then used to extrapolate the location of storms into the future.  

Google Big Query
==============================
* BigQuery is a fully managed enterprise data warehouse that helps you manage and analyze your data with built-in features like machine learning, geospatial analysis, and business intelligence.
* BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage choices. BigQuery interfaces include Google Cloud Console interface and the BigQuery command-line tool. 

Google Data Studio
==============================
* Data Studio is Google’s reporting solution for power users who want to go beyond the data and dashboards of Google Analytics. The data widgets in Data Studio are notable for their variety, customization options, live data and interactive controls 
* Data visualization tools can help you make sense of your BigQuery data and help you analyze the data interactively. You can use visualization tools to help you identify trends, respond to them, and make predictions using your data. In this tutorial, you use Google Data Studio to visualize data in the BigQuery natality sample table.

Web Application - Location based Nowcasting
=============================================

* In this Application, we are generating the predicted images using the nowcast model by calling an API. The application asks the user to input Latitude & Longitude along with the distance based on how far they want to see the storm prediction view the predicted images along with City, State, Date, and Time. The user can mention if they would like fresh data or cached data as well as the acceptable threshold time in minuts. After giving the input we can generate the images using the nowcast model by invoking the API.

NLP - Summarization & Named Entity Recognition
===============================================

* We have used pre-trained models from the Huggingface library for Summarization and NER. These models have been dockerized and the docker images uploaded to Amazon ECR.
* From ECR the images are deployed to Lambda functions using the serverless framework. The tutorial was followed as per : https://www.philschmid.de/serverless-bert-with-huggingface-aws-lambda-docker
* The Summarization Pipeline is available at :https://26tn29om40.execute-api.us-east-1.amazonaws.com/dev/qa
* The NER pipeline is available at :https://0gaq5aa6r2.execute-api.us-east-1.amazonaws.com/dev/qa

Docker
==============================

* Docker is a software platform that allows you to build, test, and deploy applications quickly. Docker packages software into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime. Using Docker, you can quickly deploy and scale applications into any environment and know your code will run.

* Docker images contain all the dependencies needed to execute code inside a container, so containers that move between Docker environments with the same OS work with no changes. Docker uses resource isolation in the OS kernel to run multiple containers on the same OS.


JWT - Authorization
==============================

* JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

* The process flow on the UI lets a user enter their username and password and the App authenticates them against the list of existing users in a BigQuery table, and if they are an approved user with an associated token, they are allowed to login and use the Nowcasting application.



Requirements
==============================
* Python 3.7
* Jupyter Notebooks
* Google Cloud Account
* AWS
* Docker
* Streamlit
* Postman
* GCPAppEngine
* Big Query
* Data Studio



Technical Specifications Document
==============================
This is the link to open the CLAAT document:
https://codelabs-preview.appspot.com/?file_id=1zeVjMrEuRsXl2Kw44M7lcJT9RFgQogadfa9tR4pkBTo#0

User Manual for the WebApp
==============================
https://codelabs-preview.appspot.com/?file_id=1v0RMU7Byf4xneCxlZU65J7qaP7Vrvj13a7cU1FBBCCk#4

Streamlit Repository
==============================
Since Streamlit webhosting requires the repository be a public one, we have created a separate public repository to store our Streamlit webapp code. Below is the link to the repository:

https://github.com/Sairaghav1999/streamlit

Project Organization
------------

```bash
├── LICENSE
├── Makefile
├── NLP_NamedEntityRecognition
│   ├── Dockerfile
│   ├── functions
│   │   └── get_model.py
│   ├── handler.py
│   ├── model
│   ├── requirements.txt
│   └── serverless.yml
├── NLP_Summarization
│   ├── Dockerfile
│   ├── functions
│   │   └── get_model.py
│   ├── handler.py
│   ├── model
│   ├── requirements.txt
│   └── serverless.yml
├── README.md
├── docs
│   ├── Makefile
│   ├── commands.rst
│   ├── conf.py
│   ├── getting-started.rst
│   ├── index.rst
│   └── make.bat
├── models
├── notebooks
├── references
├── reports
│   └── figures
├── requirements.txt
├── runtime.txt
├── setup.py
├── sevir.py
├── src
│   ├── __init__.py
│   ├── airflow_scripts
│   │   ├── HitModel.py
│   │   ├── SaveData.py
│   │   ├── SelectLatLong.py
│   │   └── Sevir_Caching.py
│   ├── data
│   ├── features
│   │   ├── __init__.py
│   │   └── build_features.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── predict_model.py
│   │   └── train_model.py
│   ├── scripts
│   │   ├── CATALOG.csv
│   │   ├── __pycache__
│   │   │   ├── app1.cpython-39.pyc
│   │   │   ├── app2.cpython-39.pyc
│   │   │   ├── auth_bearer.cpython-39.pyc
│   │   │   ├── auth_handler.cpython-39.pyc
│   │   │   ├── catalog_search.cpython-38.pyc
│   │   │   ├── catalog_search.cpython-39.pyc
│   │   │   ├── main.cpython-38.pyc
│   │   │   ├── main.cpython-39.pyc
│   │   │   ├── make_nowcast_dataset.cpython-38.pyc
│   │   │   ├── make_nowcast_dataset.cpython-39.pyc
│   │   │   ├── model.cpython-39.pyc
│   │   │   ├── multiapp.cpython-39.pyc
│   │   │   ├── nowcast.cpython-38.pyc
│   │   │   ├── nowcast.cpython-39.pyc
│   │   │   ├── nowcast_data.cpython-38.pyc
│   │   │   ├── nowcast_data.cpython-39.pyc
│   │   │   ├── nowcast_generator.cpython-38.pyc
│   │   │   ├── nowcast_generator.cpython-39.pyc
│   │   │   ├── utils.cpython-38.pyc
│   │   │   └── utils.cpython-39.pyc
│   │   ├── app.yaml
│   │   ├── auth
│   │   │   ├── __pycache__
│   │   │   │   ├── auth_bearer.cpython-38.pyc
│   │   │   │   ├── auth_bearer.cpython-39.pyc
│   │   │   │   ├── auth_handler.cpython-38.pyc
│   │   │   │   ├── auth_handler.cpython-39.pyc
│   │   │   │   ├── model.cpython-38.pyc
│   │   │   │   └── model.cpython-39.pyc
│   │   │   ├── auth_bearer.py
│   │   │   ├── auth_handler.py
│   │   │   └── model.py
│   │   ├── catalog_search.py
│   │   ├── cloud_storage_creds.json
│   │   ├── main.py
│   │   ├── make_nowcast_dataset.py
│   │   ├── nowcast.py
│   │   ├── nowcast_data.py
│   │   ├── nowcast_generator.py
│   │   ├── nowcast_reader.py
│   │   ├── requirements.txt
│   │   └── utils.py
│   └── visualization
│       ├── __init__.py
│       └── visualize.py
├── structure.json
├── test_environment.py
└── testcases.json


```

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

Contributions Statement
==============================
Below are the contributions by the team members to create this App:

1.Shika – 35%

* Python Logic – Extract event narratives and episode narratives, and call NLP APIs for summarization and NER
* GCP BigQuery - Extract Logs from logging table and preprocess data for the Dashboard
* Live Data Studio Dashboard with important metrics related to WebApp
* Summarization NLP model - Create, build, test, deploy, integrate
* NER NLP model - Build, test, deploy, integrate
* GCP hosting and debugging of API

2. Sai – 35%

* Streamlit Frontend updates
* GCP Cloud function to extract logs from logger to Bigquery in realtime
* BigQuery to store User access limits and User logs
* BigQuery debugging
* Integration Testing

3.Saketh – 30%

* NER Models research
* Documentation
* Architecture Diagram


Attestation
==============================

We attest that we have not used any other Student’s work in our code and abide by the policies listed in the Northeastern University Student Handbook regarding plagiarism and intellectual property.


