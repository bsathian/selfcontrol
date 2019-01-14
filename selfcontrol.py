#!/usr/bin/python3

import os
import sys
import subprocess
import time

def addLinesToFile(blockedListFilePath,hostsFilePath):
    '''Adds website lines from blocked.txt to /etc/hosts if not already present'''

    blockedListFile = open(blockedListFilePath,"r")
    hostsFile = open(hostsFilePath,"a")
    hostsFile.write("\n#SELFCONTROL BLOCK START\n")
    for site in blockedListFile:
        addString = site
        if site[0:4] != "www.":
            addString = "www."+addString
        hostsFile.write("0.0.0.0 " +addString)
        hostsFile.write("::0 "+addString)
    hostsFile.write("#SELFCONTROL BLOCK END\n\n")


def linesAlreadyPresent(hostsFilePath):
    '''Checks if lines are already present in hosts file'''
    hostsFile = open(hostsFilePath,"r")

    for i in hostsFile:
        if i.rstrip("\n") == "#SELFCONTROL BLOCK START":
            return True
    return False


def waitForCompletion(hh,mm):
    '''Runs a countdown timer'''
    startTime = time.time()
    currTime = time.time()
    reqTime = hh*3600+mm*60
    print("Time to Completion")
    while currTime - startTime <= reqTime:
        time.sleep(1)
        currTime = time.time()
        countdownTime = reqTime - (currTime - startTime)

        timeString = time.strftime("%H:%M:%S",time.gmtime(countdownTime))
        print(timeString,end = "\r")

def endSelfControl(hostsFilePath):
    '''Ends self control by copying the backup to the original location'''

    os.system("sudo cp hosts_backup "+hostsFilePath)

def main():
    if os.geteuid() != 0:
        subprocess.run(["sudo","python",*sys.argv])
        return
    if len(sys.argv) < 2:
        hh = 9
        mm = 0
    else:
        hh,mm = sys.argv[1].rstrip('\n').split(":")
        hh = int(hh)
        mm = int(mm)
    blockedListFilePath = "blocked.txt"
    hostsFilePath = "/etc/hosts"
    os.system("cp "+hostsFilePath+" hosts_backup")
    os.system("cp hosts_backup hosts_new")
    if not linesAlreadyPresent(hostsFilePath):
        addLinesToFile(blockedListFilePath,"hosts_new")
        os.system("cp hosts_new "+hostsFilePath)
        os.system("rm hosts_new")
    waitForCompletion(hh,mm)
    endSelfControl(hostsFilePath)

if __name__ == "__main__":
    main()

