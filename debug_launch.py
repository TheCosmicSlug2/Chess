import subprocess
import time

def launch_in_cmd(script):
    subprocess.Popen(
        f'start cmd /k python {script}',
        shell=True
    )

launch_in_cmd("web\\server.py")
time.sleep(1)
launch_in_cmd("main.py")
time.sleep(1)
launch_in_cmd("main.py")
