# Installing prerequisites (Python, Pip and Packages) 
1- Install <a href=https://www.python.org/downloads/>Python</a> version 3.6 or upper 

2- Create and activate virtual environment according to your operating system. <a href=https://help.dreamhost.com/hc/en-us/articles/115000695551-Installing-and-using-virtualenv-with-Python-3>Unix</a> and <a href=https://mothergeo-py.readthedocs.io/en/latest/development/how-to/venv-win.html>Windows</a>

3- Active or install Tkinter:
 <a href=https://docs.python.org/3/library/tkinter.html>this</a> or <a href=https://www.javatpoint.com/how-to-install-tkinter-in-python>this</a> or <a href= https://riptutorial.com/tkinter/example/3206/installation-or-setup>this</a>

4- Install packages by the following command
```
    pip install -r requirement.txt
```

# Runing server

1- Open CMD or terminal

2- Activate virtual environment mentioned before

3- Go to server directory by the following command
```
    cd server
```
4- Run server (engine)
```
    python server_main.py
```

- After all players joined the server, the game started.
- When the game finish, a JSON file is created in the `'game_logs'` directory, and you can use it for visualizing.
- You can change the configuration of the game by changing `'config.json'` in the server directory.


# Runing visualizer 
- For use visualizer, you should install Tkinter 

1- open CMD or terminal

2- Activate the virtual environment mentioned before

3- Go to server visualizer by the following command
```
    cd visualizer
```
4- Run visualizer
```
    python visualizer_main.py
```
5- Select created JSON file from `'game_logs'` directory to visualize the game



## Visualizer keys 
- **E:** Increase game speed 

- **W:** Decrease game speed

- **S:** Stopping the game

- **Q:** Quit from game

- **B:** Increase display size

- **N:** Decrease display size

- **R:** Reset game showing

# Client 

- You can use `'client_main.py'` to develop your AI code. Your code should be placed on the `'do_turn'` function.
- You can change IP and Port of server in `'client_config.json'` 


