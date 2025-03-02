from unicurses import *
import apps.main_menu as mm

config = {}
stdscr = initscr()
io_state = "command"

def init():
    noecho()
    cbreak()
    keypad(stdscr,True)
    if config["is_color"] == "True":
        start_color()
    curs_set(2)
    


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




def main_loop():
    command_string = ""
    
    while 1:
        if io_state == "command":
            io_stream = getkey()
            

pull_config()
init()

main_loop()

close()