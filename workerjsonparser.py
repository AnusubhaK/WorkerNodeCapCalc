"""
JSON Parser script to read worker information
"""

import os
import argparse
import json


def readjsonworker(filpath, WorkerList):
    filejson = open(filpath,) 
    data = json.load(filejson)
    for workerdetails in data['WorkerNodes']:
        WorkerList.append (workerdetails)
    filejson.close()


# def calcapacity():
    # for poddetails in PodList:
        # CalresDict['CPU'] = CalresDict['CPU'] + (poddetails['CPU'] * poddetails['Replicas'])
        # CalresDict['RAM'] = CalresDict['RAM'] + (poddetails['RAM'] * poddetails['Replicas'])
        # CalresDict['Storage'] = CalresDict['Storage'] + (poddetails['Storage'] * poddetails['Replicas'])
    # print("Required CPU:     " + str(CalresDict['CPU']))
    # print("Required RAM:     " + str(CalresDict['RAM']))
    # print("Required Storage: " + str(CalresDict['Storage']))


if __name__ == "__main__":
    # configuration of command line interface:
    parser = argparse.ArgumentParser(description='Script for parsing POD details using JSON outputs')
    parser.add_argument('-w', '--workerpath',required=True, help="path to JSON file with workers information")
    args = parser.parse_args()
    args_dict = vars(args)
    print("Script processing complete...")

    
    
    
    