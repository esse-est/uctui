from unicurses import *
import importlib
import logging
import time

logger = logging.getLogger(__name__)


config = {}
stdscr = initscr()
io_state = ""
loaded = {}  # dict of loaded modules


def init():
    global io_state

    get_time = time.strftime("%Y-%m-%d", time.localtime())

    if config["do_logs"] == "True":
        fh = logging.FileHandler(filename=f"logs/{get_time}.log")
        logging.basicConfig(
            format="%(asctime)s,%(msecs)d %(levelname)s %(message)s",
            level=logging.INFO,
            handlers=[fh],
        )
    noecho()
    cbreak()
    keypad(stdscr, True)
    if config["is_color"] == "True":
        start_color()
    curs_set(2)
    io_state = "main_menu"


def close():
    echo()
    nocbreak()
    keypad(stdscr, False)
    endwin()


def pull_config():  # pulls config.txt, strips it, removes comments, and formats it into config: dict
    with open("config.txt", "r") as cf:
        for i in cf.readlines():
            i = i.replace("\n", "").replace(" ", "")
            if not i.startswith("#") and len(i) != 0:
                i = i.split(":")
                if len(i) == 2:
                    config[i[0]] = i[1]

    if len(config["enabled_apps"]) > 2:
        for i in config["enabled_apps"].replace("[", "").replace("]", "").split(","):
            if type(config["enabled_apps"]) != list:
                config["enabled_apps"] = []
            config["enabled_apps"].append(i)


def pull_apps():
    enabled_holder = []
    for app in config["enabled_apps"]:
        if os.path.isfile(f"apps/{app}.py"):
            loaded[app] = importlib.import_module(f"apps.{app}")
            enabled_holder.append(app)

    config["enabled_apps"] = enabled_holder  # update to remove non-existent apps


def main():
    return_direction = "main_menu"
    while True:
        if return_direction in config["enabled_apps"]:
            loaded[return_direction].main.declare_req(stdscr, config, logger)
            loaded[return_direction].main.load()

            # allows script to return to here before going elsewhere
            return_direction = loaded[return_direction].main.loop()

        elif return_direction == "NULL":
            break

        else:
            logger.critical("tried loading app not found")
            break


pull_config()
pull_apps()

init()  # unicurses stuff

main()  # effectively just "main_menu wrapper"

close()  # closes unicurses out
