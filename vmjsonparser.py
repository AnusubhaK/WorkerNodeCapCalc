"""
JSON Parser script to read worker information
"""

import os
import argparse
import json


def readjsonvm(filpath, VMList):
    filejson = open(filpath,) 
    data = json.load(filejson)
    for vmdetails in data['VirtualMachine']:
        VMList.append (vmdetails)
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
    parser.add_argument('-v', '--vmpath',required=True, help="path to JSON file with virtual machine information")
    args = parser.parse_args()
    args_dict = vars(args)
    print("Script processing complete...")

    
    
    
    