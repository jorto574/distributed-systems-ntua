import subprocess
import os

if __name__ == "__main__":
    try:
        os.chdir("server")
        subprocess.run(["python3", "app.py"])
    except:
        print("Internal error! 'server/' directory not found.")
