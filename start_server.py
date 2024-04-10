import subprocess
import os
import argparse

parser = argparse.ArgumentParser(description='')
parser.add_argument('id', type=int, help='Node id')
args = parser.parse_args()

if __name__ == "__main__":
    try:
        os.chdir("server")
    except:
        try:
            os.chdir("Blockchat/server")
        except:
            print('Internal error! File "server" not found.')
    subprocess.run(["python3", "app.py", str(args.id)])
