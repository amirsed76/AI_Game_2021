# install python and pip 
install python version 3.6 or upper 
for download : <a>https://www.python.org/downloads/ 

create and activate virtual environment:

for unix: <a>https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3

for windows : <a>https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html

active or install tkinter : <a>https://docs.python.org/3/library/tkinter.html or  <a>https://www.javatpoint.com/how-to-install-tkinter-in-python or <a> https://riptutorial.com/tkinter/example/3206/installation-or-setup



# installation packages
`pip install -r requirement.txt`

# server
## server configuration 
you can change game configuration with change content of config.json in server directory 

## run server 
open cmd or terminal 

activate virtual environment that said before

go to server directory 

`cd server`

run server (engine)

`python server_main.py`

when all player join server, game starts and creates a json file in game_logs directory and you can use it for visualizing


# visualizer 
for use visualizer you should install tkinter 
## run visualizer 
open cmd or terminal 

activate virtual environment that said before

go to visualizer directory 

`cd visualizer`

run visualizer
`python visualizer_main.py`

select game json log  and see game 

## buttons 
e => make game faster 

w => make game slower

s => stop game

# python client 
you can use python client 

for write AI code in python client,you must write code in do turn function in client_main.py and run it

##client configuration 
you can change ip and port of server in client_config.json


