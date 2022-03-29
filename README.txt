This repository includes process of deployment of your python dashboard. Dash is a python framework created by plotly for creating interactive web applications. 
Dash is written on the top of Flask, Plotly. js and React. js. With Dash, you don't have to learn HTML, CSS and Javascript in order to create interactive dashboards, 
you only need python.

The ipython script of the dashboard development is available at https://github.com/asimanshu/Global_covid-19_dashboard.

This repository mostly deals with the deployment method. Although, there are number of ways to deploy your python dashboard, but I will be discussing step by step
process of deploying it on HEROKU. Yes, heroku.Heroku is a platform as a service (PaaS) that enables developers to build, run, and operate applications entirely in the cloud.

Follow these steps to deploy your python dashboard online. In order to deploy your dashboard with this method, you need any linux distro. 
1. Before we start, we need .py file of your python script of your dashboard. Once your dashboard is ready and running at your local server, you are fine to go ahead.

2. Make a directory with suitable name and moce your .py file into the directory. You can do it on the linux terminal with the following cammands:
	$ mkdir 'directory_name'
	$ cd 'directory_name'
	$ mv /home/app.py /home/directory_name/app.py     ### remember to save your .py file as app.py ###
3. Initialize the directory with empty git repo and activate a virtual environment by following these commands on your terminal
	$ git init
	$ virtualenv venv   ### you can name your virtual environment anything you want, venv is widely used###
	$ source venv/bin/activate    ### To activate your virtual environment
	### Once the virtual environment is activated, you would be abe to see (venv)(base) in your terminal
4. Create .gitignore file by pasting the lines below and save the file as .gitignore (no prefix is required).
	venv
	*.pyc
	.DS_Store
	.env
	### If you are using a virtual environment with a different name you should change it in the .gitignore file.
5. Create a Procfile by pasting the following line to a text file and save it as Procfile (no extension required)
	web: gunicorn app:server
6. Create a requirements.txt file by following this command
	$ pip freeze > requirements.txt
	### This command will automatically populate the files with packages that are required for the dashboard to run.
	### You must check your requirements.txt file if all the packages required for successfully running the dashboard are automatically.
	### In any case if that does not work for you, you can work with pipreqs. If it is not installed you can install it and run by following commands.
	$ pip install pipreqs
	$ pipreqs
	### This will automatically creates your requirements.txt.
	### Check if your requirements.txt file has gunicorn or not. if not you must mention it yourself (gunicorn==19.0.0 or anyother version you like). 
	### Gunicorn is required for deployment
7. Install all the packages in the requirements.txt file in your environment.
	$ pip install -r requirements.txt  ### It will install all the packages required for deploying and running your dashboard.
8. You can also create runtime file to confirm the version of python, while deploying (sometimes its good to metion your python version, which is useful during deployment).
	### to create a runtime file paste 'python==3.10.3' in your text file and save it as cat runtime.txt
9. Create an app on your heroku account with the name you like. you can do it either by logging in to heroku.com or by CLI. For CLI follow the command below:
	$ heroku create 'dashboard_name_you_wish' ### If you have not logged in, it may ask you to log in. So follow the command below to log in:
	$ heroku login      ### Provide your credentials
	$ heroku create 'dashboard_name_you_wish'
10. Deploy heroku: Follow the commands below to deploy your dashboard.
	$ git add .
	$ git commit -m ‘…’
	$ git push heroku master     ### It may take several attempts to deploy it successfully. So you have to be careful in every step.
	$ heroku ps:scale web=1
10.   When you make some changes in the any of the file in your directory and want to update it, follow these commands in your terminal:
	$ git add .
	$ git commit -m ‘…’
	$ git push heroku master 

Although deploying on heroku is a very straight forward process but sometimes it may takes several attempts before it successfully deploys it.
If you have all the files in order and error free, it shouldn't take too many attempts. However, the plus side is, once it is uploaded it is extremely simple and fast
to update.

Another negative side of the herokuapp is, it takes longer than expected to open. The reason behind it is that it sleeps after half an hour of inactivity.

You can visit my dashboard at : https://aseem-cov-dash.herokuapp.com/ 
