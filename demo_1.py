import time
import platform
import pyautogui as pg

pg.FAILSAFE = True
pg.PAUSE = 0.25  # short delay after each call

SEARCH_TERM = "today weather"

# Using Google's "I'm Feeling Lucky" so it opens the first result directly
LUCKY_URL = f"https://www.google.com/search?q={SEARCH_TERM.replace(' ', '%20')}&btnI=I"

APP_LAUNCH_WAIT = 3.5
NAV_WAIT = 2.5

def open_edge():
    system = platform.system()

    if system == "Windows":
        # Open Start → type 'msedge' → Enter
        pg.press("winleft")
        time.sleep(0.4)
        pg.typewrite("msedge")
        time.sleep(0.5)
        pg.press("enter")
        time.sleep(APP_LAUNCH_WAIT)

        # Focus Edge address bar
        pg.hotkey("ctrl", "l")
        time.sleep(0.4)

    elif system == "Darwin":  # macOS
        # Spotlight → type 'Microsoft Edge' → Enter
        pg.hotkey("command", "space")
        time.sleep(0.4)
        pg.typewrite("Microsoft Edge")
        time.sleep(0.6)
        pg.press("enter")
        time.sleep(APP_LAUNCH_WAIT)

        pg.hotkey("command", "l")
        time.sleep(0.4)

    else:  # Linux
        # Open Edge via app launcher (assumes 'microsoft-edge' command)
        pg.press("winleft")
        time.sleep(0.4)
        pg.typewrite("microsoft-edge")
        time.sleep(0.5)
        pg.press("enter")
        time.sleep(APP_LAUNCH_WAIT)

        pg.hotkey("ctrl", "l")
        time.sleep(0.4)

def search_weather():
    # Type the Lucky URL and press Enter
    pg.typewrite(LUCKY_URL, interval=0.02)
    pg.press("enter")
    time.sleep(NAV_WAIT + 2.0)  # wait for page load

def main():
    open_edge()
    search_weather()

if __name__ == "__main__":
    main()
