import time
import app.screen as screen

tick = 0
screen

def setup(functionToCall):
    global tick, screen
    screen.setup()

    try:
        while True:
            screen.clear()
            tick = (tick + 1)
            functionToCall(screen)
            screen.render()
            time.sleep(1)
    except KeyboardInterrupt:
        screen.clear()

def get_tick():
    global tick
    return tick