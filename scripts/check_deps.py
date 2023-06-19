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

def check_all_deps():
    conda_result = check_conda()
    ont_check = check_ont_deps()
    docker_images_result = check_docker_images()
    pip_deps_result = check_pip_deps()
    local_database_result = check_local_database()
    google_chrome_result = check_google_chrome()
    app_build_result = check_app_build()
    v_env_result = check_virtual_env()

    print("\n")
    print("Total dependencies check result:")

    check_list = ["ONT dependencies", "Docker images", "Pip dependencies", "Google Chrome", "Local App", "Conda", "Local software", "Local databases"]
    approved = 0
    for item in check_list:
        if item == "ONT dependencies":
            if ont_check:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
        elif item == "Docker images":
            if docker_images_result:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
        elif item == "Pip dependencies":
            if pip_deps_result:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
        elif item == "Google Chrome":
            if google_chrome_result:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(item + " is not installed")
        elif item == "Local App":
            if app_build_result:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
        elif item == "Conda":
            if conda_result:
                print(bcolors.OKGREEN + item + " is installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
        elif item == "Local software":
            if local_software_result:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
        elif item == "Local databases":
            if local_database_result:
                print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
                approved += 1
            else:
                print(bcolors.FAIL + item + " is not installed" + bcolors.ENDC)
    if len(check_list) == approved:
        print(bcolors.OKGREEN + "All dependencies are installed and lpf is ready for use." + bcolors.ENDC)

def check_ont_deps():
    """
    check_list = [
        '/opt/ont',
        '/opt/ont/guppy',
        '/opt/ont/minknow',
        '/lib/systemd/system/guppyd.service'
    ]
    for item in check_list:
        if os.path.exists(item):
            print(bcolors.OKGREEN + item + " are installed" + bcolors.ENDC)
        else:
            print(item + " is not installed")
            return False
    """
    #Temporary disable ONT check
    return True

def check_pip_deps():
    pip_list = list()
    with open('resources/requirements.txt') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#"):
                continue
            if '>' in line:
                line = line.split('>')[0]
                pip_list.append(line)
            elif '<' in line:
                line = line.split('<')[0]
                pip_list.append(line)
            elif '==' in line:
                line = line.split('==')[0]
                pip_list.append(line)
            else:
                pip_list.append(line)

    proc = subprocess.Popen("pip list", shell=True,
                            stdout=subprocess.PIPE, )
    output = proc.communicate()[0].decode().split("\n")
    for item in output[0:-1]:
        item = item.split()
        name = item[0]
        if name in pip_list:
            print(bcolors.OKGREEN + name + " is installed" + bcolors.ENDC)
            pip_list.remove(name)
    if len(pip_list) > 0:
        print("The following pip packages are missing:")
        for item in pip_list:
            print(item)
        return False
    else:
        return True

def check_local_database():
    if not os.path.exists('/opt/lpf_databases/resfinder_db/resfinder_db.name'):
        print(bcolors.FAIL + "Resfinder database not found" + bcolors.ENDC)
        return False
    if not os.path.exists('/opt/lpf_databases/plasmidfinder_db/plasmidfinder_db.name'):
        print(bcolors.FAIL + "Plasmidfinder database not found" + bcolors.ENDC)
        return False
    if not os.path.exists('/opt/lpf_databases/virulencefinder_db/virulencefinder_db.name'):
        print(bcolors.FAIL + "Virulencefinder database not found" + bcolors.ENDC)
        return False
    if not os.path.exists('/opt/lpf_databases/mlst_db/ecoli/'):
        print(bcolors.FAIL + "MLST database not found" + bcolors.ENDC)
        return False
    if not os.path.exists('/opt/lpf_databases/bacteria_db/bacteria_db.name'):
        print(bcolors.FAIL + "Bacteria database not found" + bcolors.ENDC)
        return False
    #Add Viral database
    else:
        print(bcolors.OKGREEN + "All lpf databases are correctly installed." + bcolors.ENDC)
        return True

def check_docker_images():
    docker_list = list ()
    with open('resources/docker_images.txt', 'r') as f:
        for line in f:
            docker_list.append(line.strip())


    proc = subprocess.Popen("docker images", shell=True,
                            stdout=subprocess.PIPE, )
    output = proc.communicate()[0].decode().split("\n")

    if "REPOSITORY" not in output[0]:
        print("Docker is not installed")
        return False

    for item in output[0:-1]:
        item = item.split()
        name = item[0] + ":" + item[1]
        if name in docker_list:
            print(bcolors.OKGREEN + name + " are installed" + bcolors.ENDC)
            docker_list.remove(name)
    if len(docker_list) > 0:
        print("The following docker images are missing:")
        for item in docker_list:
            print(item)
        return False
    else:
        return True

def check_conda():
    home = str(Path.home())
    proc = subprocess.Popen("which conda", shell=True,
                            stdout=subprocess.PIPE, )
    conda_output = proc.communicate()[0].decode().rstrip()
    if (conda_output.startswith(home)):
        print(bcolors.OKGREEN + "Conda is installed corrently in /home/user/" + bcolors.ENDC)
        return True
    else:
        print(bcolors.FAIL + "Conda is not installed" + bcolors.ENDC)
        return False

def check_virtual_env():
    proc = subprocess.Popen("conda env list", shell=True,
                            stdout=subprocess.PIPE, )
    env = proc.communicate()[0].decode().split()
    if 'lpf' in env:
        print(bcolors.OKGREEN + "lpf environment is installed" + bcolors.ENDC)
        return True
    else:
        print(bcolors.FAIL + "lpf environment is not installed" + bcolors.ENDC)
        return False

def check_app_build():
    path_list = ["/opt/lpf_app/dist/linux_unpacked/lpf"]
    for item in path_list:
        if not os.path.exists(item):
            print(bcolors.FAIL+ item +" is not installed" + bcolors.ENDC)
            return False
    if check_dist_build():
        return True
    else:
        return False

def check_google_chrome():
    proc = subprocess.Popen("apt list --installed | grep \"google-chrome\"", shell=True,
                            stdout=subprocess.PIPE, )
    output = proc.communicate()[0].decode().split("\n")
    for item in output[0:-1]:
        if item.startswith("google-chrome"):
            return True
    return False

def check_virtual_env():
    proc = subprocess.Popen("conda env list", shell=True,
                            stdout=subprocess.PIPE, )
    env = proc.communicate()[0].decode().split()
    if 'lpf' in env:
        print(bcolors.OKGREEN + "lpf environment is installed" + bcolors.ENDC)
        return True
    else:
        print(bcolors.FAIL + "lpf environment is not installed" + bcolors.ENDC)
        return False