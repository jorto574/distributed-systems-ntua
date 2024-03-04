import subprocess
import os

if __name__ == '__main__':
    os.chdir('server')
    subprocess.run(['python', 'app.py'])
