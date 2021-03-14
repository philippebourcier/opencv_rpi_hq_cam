#!/usr/bin/python3

import yaml

with open(r'/dev/shm/detector_output.run') as file:
    data=yaml.load(file,Loader=yaml.FullLoader)
    print(data)

