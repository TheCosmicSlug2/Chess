from main import main
from web.server import main as servermain
import time
import threading

threading.Thread(target=servermain, daemon=True).start()
time.sleep(1)
threading.Thread(target=main, daemon=True).start()
time.sleep(1)
threading.Thread(target=main, daemon=True).start()