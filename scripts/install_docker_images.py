import os
docker_list = list()
with open('resources/docker_images.txt', 'r') as f:
    for line in f:
        docker_list.append(line.strip())

for item in docker_list:
    cmd = "docker pull " + item
    os.system(cmd)