import os
import sys
import subprocess

sys.path = [os.path.join(os.path.dirname(os.path.realpath(__file__)),'..')] + sys.path

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

proc = subprocess.Popen("conda env list", shell=True,
                            stdout=subprocess.PIPE, )
env = proc.communicate()[0].decode().split()
print("Checking for lpf environment")
print(env)
env_file = 'resources/environment2.yml'
if not os.path.exists(env_file):
    env_file = 'scripts/resources/environment2.yml'

if 'lpf' in env:
    print("lpf environment already exists")
    print("Updating lpf environment")
    os.system("conda env update --file {}  --prune".format(env_file))
else:
    os.system("conda env create -f {}".format(env_file))

