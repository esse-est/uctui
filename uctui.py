from unicurses import *
import importlib
import logging
import time

logger = logging.getLogger(__name__)


config = {}
stdscr = initscr()
io_state = ""
loaded = {} #dict of loaded modules

def init():
    global io_state
    
    get_time=time.strftime("%Y-%m-%d", time.localtime())
    
    logging.basicConfig(filename=f"logs/{get_time}.log",
                        encoding="utf-8",
                        level=logging.DEBUG)
    
    noecho()
    cbreak()
    keypad(stdscr,True)
    if config["is_color"] == "True":
        start_color()
    curs_set(2)
    io_state = "main_menu"

def close():
    echo()
    nocbreak()
    keypad(stdscr,False)
    endwin()

def pull_config(): #pulls config.txt, strips it, removes comments, and formats it into config: dict
    with open("config.txt", "r") as cf:
        for i in cf.readlines():
            i=i.replace("\n","").replace(" ", "")
            if not i.startswith("#") and len(i) != 0:
                i=i.split(":")
                if len(i) == 2:
                    config[i[0]] = i[1]
    
    if len(config["enabled_apps"]) > 2:
        for i in config["enabled_apps"].replace("[", "").replace("]", "").split(","):
            if type(config["enabled_apps"]) != list:
                config["enabled_apps"] = []
            config["enabled_apps"].append(i)

def pull_apps():
    for app in config["enabled_apps"]:
        if os.path.isfile(f"apps/{app}.py"):
            loaded[app] = importlib.import_module(f"apps.{app}")
            loaded[app].main.loop()
        print(loaded)

def main():
    command_string = ""
    
    if "main_menu" in loaded:
        loaded["main_menu"].main.declare_req(stdscr,logger)
        loaded["main_menu"].main.load()
        
        loaded["main_menu"].main.loop()

pull_config()
pull_apps()

init() #unicurses stuff

main() #effectively just "main_menu wrapper"

close() #closes unicurses out