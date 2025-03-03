from unicurses import *

io_command = ""

def x_at_half(string=""):
    if len(string) != 0: #so empty string doesnt crash
        location = (getmaxx(window)//2)-len(string)//2
    else:
        location = (getmaxx(window)//2)
    return(location)

class main:
    
    
    def declare_req(box: str, source_config: dict, source_logger):
        global window, logger, config
        window = box
        logger = source_logger
        config = source_config
    
    def load():
        
        y_max,x_max = getmaxyx(window)
        clear()
        mvaddstr(0,x_at_half("main_menu"),"main_menu",A_BOLD)
        
        #building window boxes, note box()/border() not used as its 1 scr
        setsyx(1,x_at_half())
        vline("|",y_max-2)
        setsyx(1,0)
        hline("-",x_max)
        
        #bad math for 1 liners T-T
        mvaddstr(2,(x_max//4-(len("Loaded Apps:")//2)),"Loaded Apps:",A_BOLD)
        app_counter = 0
        for i in config["enabled_apps"]:
            if app_counter < y_max:
                app_counter+=1
                mvaddstr((app_counter+2),(x_max//4-(len(i)//2)),i)
        
        
        mvaddstr(2,(round(x_max*0.75)-len("Commands:")//2),"Commands:",A_BOLD)
        
        
        setsyx(getmaxy(window)-1,0)
        addstr("to_run:",A_BOLD)
        
        logger.debug("main_menu module init")


    def loop():
        global io_command
        
        while True:
            y, x = getsyx()
            io_stream = getkey()
            
            io_command=io_command.strip()
            
            if len(io_stream) == 1:
                addch(io_stream)
                io_command += io_stream
            
            elif io_stream == "KEY_BACKSPACE" and getsyx()[1] > 7:
                io_command = io_command[:-1]
                mvaddstr(y,x-1," ")
                setsyx(y,x-1)
            
            elif io_stream == "^J" and len(io_stream) != 0: #running a command
                
                if io_command.startswith("load"): #extra if for load() as y'need the name
                    load_split = io_command.split("*")
                    if len(load_split) == 3 and len(load_split[1]) != 0:
                        commands.load(io_command.split("*")[1])
                
                #has to be here as return() needs to be in loop()
                elif io_command == "quit": 
                    return("NULL")
                
                elif io_command.lower() in commands.user_alias:
                    commands.user_alias[io_command]()
                else:
                    logger.warning("user tried to run erroring command")
                
                mvaddstr(y,7,(" "*len(io_command)))
                
                setsyx(y,7)

class commands:
    global command_list
    
    def load(app: str):
        if os.path.isfile(f"apps/{app}.py"):
            return(app)
        else:
            logger.warning("user tried to load non-existent app")
    
    def config():
        pass

    
    user_alias = {"load": load
                    , "cfg": config} #user typed strs for ran commands