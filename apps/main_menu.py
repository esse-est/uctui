from unicurses import *

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
        
        logger.debug("main_menu module init")


    def loop():
        
        while 1:
            y, x = getsyx()
            
            io_stream = getkey()
            