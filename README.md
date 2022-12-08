# Netbox
A python simple and flexible CLI tool used to network testing.

# Introduction
This command line tool integrates some common network operations, such as wireless network connection, network ping, network speed measurement, etc., which can be done by using simple commands. The tool supports cross-platform, consistent command-line style for the three major operating systems and user-friendly. In addition, the tool provides a rich function interface which is convenient for users to integrate according to the actual business.

# Getting Started
## Prerequisites
* Install python3 on your local machine, no matter what operating system you are using, you can refer to the link as below

	[How to install python3](https://realpython.com/installing-python/)
* Install git on your local machine, no matter what operating system you are using, you can refer to the link as below

	[How to install git](https://git-scm.com/)
	
## Installing
A step by step series of examples that tell you how to get the CLI tool running.

### Installing via git repository
1. Clone project with git command

	```shell
	git clone https://github.com/Hellboycc/netbox.git
	
	```
2. Create a virtual environment in the project root directory

	```shell
	cd netbox
	python -m venv .venv
	```
3. Activate current virtual environment

	```shell
	# For MacOS
	cd .venv/bin
	source activate
	```
4. Install all dependency with pip3 command

	```shell
	# In this path /Users/..../netbox
	pip3 install -r requirements.txt
	```
5. Install project on your local machine

	```shell
	# In this path /Users/..../netbox 
	pip3 install -e .
	```
	
### Installing from pypi
If you don't want to use git repository, you could choose to download from [pypi.org](https://pypi.org/project/netbox/0.0.1/) and install to use.

```shell
pip3 install netbox
```
	
### Running CLI on your terminal window
1. Example for display CLI tool information
	
	```shell
	netbox-cli                                                                                                                                                                    
	Usage: netbox-cli [OPTIONS] COMMAND [ARGS]...
	
	  A simple and flexible CLI tool for network testing
	
	Options:
	  --version  Print version information and quit
	  --help     Show this message and exit.
	
	Commands:
	  version  Show the CLI tool version information
	  wlan     Manage wifi network
	```
2. Example for child commands
	
	```shell
	netbox-cli wlan                                                                                                                                                              
	Usage: netbox-cli wlan [OPTIONS] COMMAND [ARGS]...
	
	  Manage wifi network
	
	Options:
	  --help  Show this message and exit.
	
	Commands:
	  connect     Connect a wifi network
	  current     Current wifi network information
	  disconnect  Disconnect current wifi network
	  scan        Scan surround wifi network
	```
3. Example for dispaly current version

	```shell
	netbox-cli version   
	                                                                                                                                                         
	Current version is v0.0.1
	```
4. Example for scan a specified wifi network exists or not

	```shell
	netbox-cli wlan scan --ssid Hellboycc 
	                                                                                                                                        
	Current ssid Hellboycc is not found.
	```
	
# Testing
The project contains complete unit tests, if you want to know the unit test results before using the tool, you can get the detailed test results by executing the unit tests.
### How to run unit test
1. Install all dependency of develop

	```shell
	# For MacOS
	cd netbox
	python -m venv .venv
	cd .venv/bin
	source activate
	# In this path /Users/..../netbox
	pip3 install -r requirements-dev.txt
	```
2. Running unit test with tox command

	```shell
	# In this path /Users/..../netbox
	tox
	```

# FAQ & Issues
- If you encounter any problems in using it, please keep in touch with me and I will reply as soon as possible, you can access to the link as below

	[Issues of project](https://github.com/Hellboycc/netbox/issues)

- Other classic questions

	[FAQ](#)

# License
This project is licensed under the MIT License (see the [LICENSE](https://choosealicense.com/licenses/mit/) file for details).