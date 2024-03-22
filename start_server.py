import subprocess
import os

if __name__ == "__main__":
    try:
        os.chdir("server")
    except:
        try:
            os.chdir("Blockchat/server")
        except:
            print('Internal error! File "server" not found.')
    subprocess.run(["python3", "app.py"])
