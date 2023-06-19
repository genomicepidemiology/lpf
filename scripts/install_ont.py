import os

os.system("sudo apt update")
os.system("wget http://apt.zwets.it/debs/kcri-apt-repo_1.0.0_all.deb")
os.system("sudo apt update")
os.system("sudo apt install ./kcri-apt-repo_1.0.0_all.deb")
os.system("sudo apt update")
os.system("sudo apt install kcri-seqtz-repos")
os.system("sudo apt update")
os.system("wget http://apt.zwets.it/debs/kcri-seqtz-deps_1.3.0_amd64.deb")
os.system("sudo apt install ./kcri-seqtz-deps_1.3.0_amd64.deb")
os.system("sudo apt update")
os.system('rm kcri-*')
os.system('sudo groupadd docker; sudo usermod -aG docker $USER; sudo chmod 666 /var/run/docker.sock')