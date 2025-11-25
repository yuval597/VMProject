Infra-Automation project v1.0

# Overview
This project is an infrastructure provisioning simulator written in Python
It allows the user to create virtual machines (VMs), saves it into JSON file and then install NGINX

# Project Objectives
-Ask for machine details (Name,OS,CPU,RAM)
-Validate the input using Pydantic
-Saving all machines into file "instances.json"
-Running a bash script that installs NGINX or skips incase its already installed
-Everything written into logs/provisioning.log

# Setup
-Clone the repository
-Create virtual environment
-Install the required python packages from requirements.txt
-Run the program