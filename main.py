"""
JSON Parser script to read POD information
"""

import os
import argparse
import math
from podjsonparser import readjsonpod, calpodtotalcapacity
from workerjsonparser import readjsonworker
from vmjsonparser import readjsonvm


# Define global variables for processing
PodList = []
WorkerNodeList = []
VirtualMachineList = []

CalcPodLoadDict = {
                "CPU": 0,
                "RAM": 0,
                "Storage": 0,
}

CalcReqWorkersDict = {
                "CPU": 0,
                "RAM": 0,
                "Storage": 0,
                "Count": 0
}

#function calculates total workers required
def calcrequiredworkers(bufpercent):
    calpodtotalcapacity(PodList, CalcPodLoadDict) 
    
    # Calcualte available resourse excluding buffers. floor rounds down decimal to integer
    WorkerActCPU = math.floor(WorkerNodeList[0]['CPU'] * 0.9)
    WorkerActRAM = math.floor(WorkerNodeList[0]['RAM'] * 0.9)
    WorkerActStorage = math.floor(WorkerNodeList[0]['Storage'] * 0.9)

    # Calcualte total CPU, RAM, Storage required from worker. ceil rounds up decimal to integer    
    CalcReqWorkersDict['CPU'] = math.ceil(CalcPodLoadDict['CPU'] / WorkerActCPU)
    CalcReqWorkersDict['RAM'] = math.ceil(CalcPodLoadDict['RAM'] / WorkerActRAM)
    CalcReqWorkersDict['Storage'] = math.ceil(CalcPodLoadDict['Storage'] / WorkerActStorage)
    
    # Find largest of the 3 resourse, which is the total number of workers required
    if (CalcReqWorkersDict['CPU'] >= CalcReqWorkersDict['RAM']) and (CalcReqWorkersDict['CPU'] >= CalcReqWorkersDict['Storage']):
        CalcReqWorkersDict['Count'] = CalcReqWorkersDict['CPU']
    elif (CalcReqWorkersDict['RAM'] >= CalcReqWorkersDict['CPU']) and (CalcReqWorkersDict['RAM'] >= CalcReqWorkersDict['Storage']):
        CalcReqWorkersDict['Count'] = CalcReqWorkersDict['RAM']
    else:
        CalcReqWorkersDict['Count'] = CalcReqWorkersDict['Storage']



if __name__ == "__main__":

    # configuration of command line interface:
    parser = argparse.ArgumentParser(description='Script for parsing POD details using JSON outputs')
    parser.add_argument('-p', '--podpath',required=True, help="path to JSON file with pod information")
    parser.add_argument('-w', '--workerpath',required=True, help="path to JSON file with workers information")
    parser.add_argument('-v', '--vmpath',required=True, help="path to JSON file with virtual machine information")
    #parser.add_argument('-b', '--buffer',type=int, default=90, help="reserved buffer in percentage to consider per worker")
    parser.add_argument('-o', '--outfile',required=True, help="path to output file to write the results")
    args = parser.parse_args()
    args_dict = vars(args)

    #Read input JSON files
    readjsonpod(args.podpath, PodList)
    readjsonworker(args.workerpath, WorkerNodeList)
    readjsonvm(args.vmpath, VirtualMachineList)

    ResultFile = open(args.outfile, "w") 
    
    #Calcualtions
    calcrequiredworkers(args.buffer)
    

    ResultFile.write ("-----------------------------------------------------------------\n")       
    ResultFile.write ("               Worker Node Calculation Script                    \n")
    ResultFile.write ("-----------------------------------------------------------------\n")
    ResultFile.write ("Input: Pod Details: \n")
    ResultFile.write ("    Total Pods: " + str(len(PodList)) + "\n")
    ResultFile.write ("    Required CPU:      " + str(CalcPodLoadDict['CPU']) + "\n")
    ResultFile.write ("    Required RAM:      " + str(CalcPodLoadDict['RAM']) + "\n")
    ResultFile.write ("    Required Storage:  " + str(CalcPodLoadDict['Storage']) + "\n\n")

    ResultFile.write ("Input: Worker Details: \n")
    ResultFile.write ("    Total Workers: 1\n")
    ResultFile.write ("    Available CPU:     " + str(WorkerNodeList[0]['CPU']) + "\n")
    ResultFile.write ("    Available RAM:     " + str(WorkerNodeList[0]['RAM']) + "\n")
    ResultFile.write ("    Available Storage: " + str(WorkerNodeList[0]['Storage']) + "\n")
    ResultFile.write ("-----------------------------------------------------------------\n")

    ResultFile.write ("Result: Required Worker Nodes:: \n")
    ResultFile.write ("    Minimum Required Worker Nodes: " + str(CalcReqWorkersDict['Count']) + " with buffer as " + str(args.buffer) + " percent per worker\n\n")
    # ResultFile.write ("    Total CPU/Worker:     " + str(CalcReqWorkersDict['CPU']) + "\n")
    # ResultFile.write ("    Total RAM/Worker:     " + str(CalcReqWorkersDict['RAM']) + "\n")
    # ResultFile.write ("    Total Storage/Worker: " + str(CalcReqWorkersDict['Storage']) + "\n")
    ResultFile.write ("-----------------------------------------------------------------\n")
    
    ResultFile.close()
    print("\nMinimum Required Worker Nodes: " + str(CalcReqWorkersDict['Count']) + " with buffer as " + str(args.buffer) + " percent per worker")
    print("Script processing complete...")

    
    
    
    
