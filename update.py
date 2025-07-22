# update.py
import os
import subprocess

REPO_DIR = '/path/to/your/repo'

def update_repo():
    os.chdir(REPO_DIR)
    subprocess.run(['git', 'pull'])

if __name__ == '__main__':
    update_repo()
